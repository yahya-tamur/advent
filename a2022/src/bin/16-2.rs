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
//one 'message' per message was too slow -- too many messages
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
//The load seems to be well-balanced from the logs we see
//though.
//

use regex::Regex;
use std::cmp::{max, min};
use std::collections::HashMap;

use std::sync::{Arc, Condvar, Mutex};
use std::thread;

#[cfg(feature = "log16_2")]
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

struct Message {
    score: usize,
    node1: usize,
    node2: usize,
    time1: usize,
    time2: usize,
    state: u32,
}

struct MT {
    waiting: u8,
    max: usize,
    messages: Vec<Message>,
}

#[cfg(feature = "log16_2")]
#[derive(Default)]
struct Logs {
    states_processed: usize,
    used_channel: usize,
    put_into_channel: usize,
    woke_up: usize,
    waited: u128,
}

#[cfg(feature = "log16_2")]
impl std::fmt::Display for Logs {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "I processed {} states. ", self.states_processed)?;
        write!(f, "I used the channel {} times. ", self.used_channel)?;
        write!(
            f,
            "I put into the channel {} times. ",
            self.put_into_channel
        )?;
        write!(f, "I woke up {} times. ", self.woke_up)?;
        write!(f, "I waited {} milliseconds.", self.waited / 1_000_000)?;
        Ok(())
    }
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

    let glob_states: Arc<(Mutex<MT>, Condvar)> = Arc::new((
        Mutex::new(MT {
            waiting: 0,
            max: 0,
            messages: vec![Message {
                score: 0,
                node1: start,
                node2: start,
                time1: 0,
                time2: 0,
                state: ((1 << nix.len()) - 1) ^ (1 << start),
            }],
        }),
        Condvar::new(),
    ));

    thread::scope(|s| {
        for _ in 0..NUM_THREADS {
            s.spawn(|| {
                #[cfg(feature = "log16_2")]
                let mut logs = Logs::default();

                let mut my_states = Vec::<Message>::new();
                let mut my_max = 0;
                let pair = Arc::clone(&glob_states);
                loop {
                    #[cfg(feature = "log16_2")]
                    {
                        logs.used_channel += 1;
                    }
                    {
                        let (lock, cv) = &*pair;
                        let mut mutex = lock.lock().unwrap();
                        mutex.waiting += 1;
                        #[cfg(feature = "log16_2")]
                        let started = SystemTime::now();
                        while (*mutex.messages).is_empty() {
                            if mutex.waiting == NUM_THREADS {
                                #[cfg(feature = "log16_2")]
                                {
                                    logs.waited += SystemTime::now()
                                        .duration_since(started)
                                        .unwrap()
                                        .as_nanos();
                                    println!("{logs}");
                                }
                                {
                                    mutex.max = max(my_max, mutex.max);
                                }

                                cv.notify_all();
                                return;
                            }
                            mutex = cv.wait(mutex).unwrap();
                            #[cfg(feature = "log16_2")]
                            {
                                logs.woke_up += 1;
                            }
                        }
                        #[cfg(feature = "log16_2")]
                        {
                            logs.waited += SystemTime::now()
                                .duration_since(started)
                                .unwrap()
                                .as_nanos();
                        }
                        mutex.waiting -= 1;
                        for _ in 0..3 {
                            if let Some(m) = mutex.messages.pop() {
                                my_states.push(m);
                            } else {
                                break;
                            }
                        }
                    }

                    while let Some(m) = my_states.pop() {
                        #[cfg(feature = "log16_2")]
                        {
                            logs.states_processed += 1;
                        }
                        for newnode in 0..nix.len() {
                            if m.state & (1 << newnode) == 0 {
                                continue;
                            }
                            let newtime1 = m.time1 + npaths[m.node1][newnode] + 1;

                            if newtime1 > 26 {
                                continue;
                            }

                            let newscore = m.score + graph[nix[newnode]].flow * (26 - newtime1);
                            let newstate = m.state ^ (1 << newnode);
                            if newstate == 0 {
                                continue;
                            }
                            my_max = max(my_max, newscore);
                            let new_message = if newtime1 > m.time2 {
                                Message {
                                    score: newscore,
                                    node1: m.node2,
                                    node2: newnode,
                                    time1: m.time2,
                                    time2: newtime1,
                                    state: newstate,
                                }
                            } else {
                                Message {
                                    score: newscore,
                                    node1: newnode,
                                    node2: m.node2,
                                    time1: newtime1,
                                    time2: m.time2,
                                    state: newstate,
                                }
                            };
                            if my_states.len() > 50 {
                                #[cfg(feature = "log16_2")]
                                {
                                    logs.put_into_channel += 1;
                                }
                                let (lock, cv) = &*pair;
                                let mut mutex = lock.lock().unwrap();
                                mutex.messages.append(&mut my_states.split_off(10));
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
    let (lock, _cv) = &*(glob_states);
    let l = lock.lock().unwrap();
    println!("part 2: {}", l.max);
}
