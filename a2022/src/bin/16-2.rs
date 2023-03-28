//Uses Floyd-Warshall (all sources shortest paths)
//to create a much smaller total graph with no 0-nodes.
//there each 'step' is taking the optimal path to some
//open valve and opening it.
//then uses naive dfs to find highest cost path through
//that graph.
//uses interesting heuristic to make part 2 solution
//very similar to part 1.
//
//my first solution was slower on both parts, about 12
//seconds total on 20 cores. It used something similar to
//dynamic programming, but had a lot of states to memoize,
//making it very inefficient. However, it made good use of
//all the cores.
//
//For this solution, using an out-of-the-box channel with
//one 'state' per message was too slow -- too many messages
//need to be sent, and the work needed per message was
//comparitively quick.
//
//I implemented a basic load-sharing channel using concurrency
//primitives. Doing this in Rust was a lot nicer than what
//I'm used to from C or C++.
//
//It runs in about 1 second with 20 cores, versus about 10
//seconds with 1 core, on my computer. However, it's a
//very short runtime start to end, so I don't have time to
//see the cores spin up and then back down again, at least
//on htop.
//The load seems to be well-balanced from the 'logs' we see
//though.
//

use regex::Regex;
use std::cmp::{max, min};
use std::collections::HashMap;

use std::sync::{Arc, Condvar, Mutex};
use std::thread;

use std::time::SystemTime;

//I feel like having this higher than the number of physical
//threads might be a good thing, since a lot of threads wait
//anyway. I can't really check though -- it runs a bit too
//fast like I mentioned.
const NUM_THREADS: u8 = 20;

#[derive(Debug)]
struct Node {
    name: String,
    flow: usize,
    tunnels: Vec<usize>,
}

fn parse(s: &str) -> Vec<Node> {
    let r = Regex::new(
        r"(?x)
    Valve\ (?P<name>.{2})\ .*
    rate=(?P<flow>\d+);.*
    valves?\ (?P<tunnels>.*)\n
    ",
    )
    .unwrap();

    let names: HashMap<String, usize> = HashMap::from_iter(
        r.captures_iter(s)
            .map(|caps| caps.name("name").unwrap().as_str().to_string())
            .enumerate()
            .map(|(i, s)| (s, i)),
    );

    r.captures_iter(s)
        .map(|caps| Node {
            name: caps.name("name").unwrap().as_str().to_string(),
            flow: caps.name("flow").unwrap().as_str().parse().unwrap(),
            tunnels: caps
                .name("tunnels")
                .unwrap()
                .as_str()
                .split(", ")
                .map(|x| *names.get(&x.to_string()).unwrap())
                .collect(),
        })
        .collect()
}

fn main() {
    let s = std::fs::read_to_string("inputs/16.txt").unwrap();
    let graph: Vec<Node> = parse(&s);

    let mut paths: Vec<Vec<usize>> = Vec::with_capacity(graph.len() - 1);
    //paths[j][i], i < j.
    for i in 0..graph.len() {
        paths.push(vec![999; i]);
    }

    for (i, n) in graph.iter().enumerate() {
        for &j in n.tunnels.iter() {
            if i < j {
                paths[j][i] = 1;
            }
        }
    }

    for j in 0..graph.len() {
        for i in 0..j {
            for k in (j + 1)..graph.len() {
                paths[k][i] = min(paths[k][i], paths[k][j] + paths[j][i]);
            }
        }
        for i in 0..j {
            for k in (i + 1)..j {
                paths[k][i] = min(paths[k][i], paths[j][k] + paths[j][i]);
            }
        }
        for i in (j + 1)..graph.len() {
            for k in (i + 1)..graph.len() {
                paths[k][i] = min(paths[k][i], paths[k][j] + paths[i][j]);
            }
        }
    }

    let nix = graph
        .iter()
        .enumerate()
        .filter(|(_i, n)| n.flow != 0 || n.name == "AA")
        .map(|(i, _n)| i)
        .collect::<Vec<usize>>();

    let mut npaths = vec![vec![999; nix.len()]; nix.len()];
    for i in 0..npaths.len() {
        for j in 0..i {
            npaths[i][j] = paths[nix[i]][nix[j]];
            npaths[j][i] = paths[nix[i]][nix[j]];
        }
    }

    let start = (0..nix.len())
        .find(|&i| graph[nix[i]].name == "AA")
        .unwrap();

    let mut max_score = 0;

    let mut states: Vec<(usize, usize, usize, u32)> =
        vec![(0, start, 0, ((1 << nix.len()) - 1) ^ (1 << start))];
    while let Some((score, current, time, state)) = states.pop() {
        for i in 0..nix.len() {
            if state & (1 << i) == 0 {
                continue;
            }
            let newtime = time + npaths[current][i] + 1;
            if newtime > 30 {
                continue;
            }
            let newscore = score + graph[nix[i]].flow * (30 - newtime);
            max_score = max(max_score, newscore);
            states.push((newscore, i, newtime, state ^ (1 << i)));
        }
    }
    println!("part 1: {max_score}");

    type Message = (usize, usize, usize, usize, usize, u32);
    let glob_max = Arc::new(Mutex::new(0));

    type MT = (u8, Vec<Message>);
    let glob_states: Arc<(Mutex<MT>, Condvar)> = Arc::new((
        Mutex::new((
            0,
            vec![(0, start, start, 0, 0, ((1 << nix.len()) - 1) ^ (1 << start))],
        )),
        Condvar::new(),
    ));

    thread::scope(|s| {
        for _ in 0..NUM_THREADS {
            s.spawn(|| {
                let mut states_processed = 0;
                let mut needed_glob = 0;
                let mut max_dumped_into_glob = 0;
                let mut woke_up = 0;
                let mut waited = 0;

                let mut my_states = Vec::<Message>::new();
                let mut my_max = 0;
                let pair = Arc::clone(&glob_states);
                loop {
                    needed_glob += 1;
                    {
                        let (lock, cv) = &*pair;
                        let mut mutex = lock.lock().unwrap();
                        mutex.0 += 1;
                        let started = SystemTime::now();
                        while (*mutex.1).is_empty() {
                            if mutex.0 == NUM_THREADS {
                                waited += SystemTime::now()
                                    .duration_since(started)
                                    .unwrap()
                                    .as_nanos();
                                {
                                    println!(
                                        "I processed {states_processed} states. \
                                            I needed the global channel {needed_glob} \
                                            times. I put into the global channel \
                                            {max_dumped_into_glob} times. I \
                                            woke up {woke_up} times. I waited \
                                            {} milliseconds.",
                                        waited / 1_000_000
                                    );
                                    let mut l = glob_max.lock().unwrap();
                                    *l = max(my_max, *l);
                                }

                                cv.notify_all();
                                return;
                            }
                            mutex = cv.wait(mutex).unwrap();
                            woke_up += 1;
                        }
                        waited += SystemTime::now()
                            .duration_since(started)
                            .unwrap()
                            .as_nanos();
                        mutex.0 -= 1;
                        for _ in 0..3 {
                            if let Some(m) = mutex.1.pop() {
                                my_states.push(m);
                            } else {
                                break;
                            }
                        }
                    }

                    while let Some((score, node1, node2, time1, time2, state)) = my_states.pop() {
                        states_processed += 1;
                        for i in 0..nix.len() {
                            if state & (1 << i) == 0 {
                                continue;
                            }
                            let newtime1 = time1 + npaths[node1][i] + 1;

                            if newtime1 > 26 {
                                continue;
                            }

                            let newscore = score + graph[nix[i]].flow * (26 - newtime1);
                            let newstate = state ^ (1 << i);
                            if newstate == 0 {
                                continue;
                            }
                            my_max = max(my_max, newscore);
                            let new_message = if newtime1 > time2 {
                                (newscore, node2, i, time2, newtime1, newstate)
                            } else {
                                (newscore, i, node2, newtime1, time2, newstate)
                            };
                            if my_states.len() > 50 {
                                max_dumped_into_glob += 1;
                                let (lock, cv) = &*pair;
                                let mut mutex = lock.lock().unwrap();
                                mutex.1.append(&mut my_states.split_off(10));
                                cv.notify_all();
                            } else {
                                my_states.push(new_message);
                            }
                        }
                    }
                }
            });
        }
    });
    let l = glob_max.lock().unwrap();
    println!("part 2: {}", l);
}
