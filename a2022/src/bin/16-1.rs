use rayon::prelude::*;
use regex::Regex;
use std::cmp::max;
use std::collections::HashMap;

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
    let s = common::get_problem(2022, 16);
    let graph: Vec<Node> = parse(&s);
    let state_nodes: HashMap<usize, usize> = HashMap::from_iter(
        graph
            .iter()
            .enumerate()
            .filter(|(_, n)| n.flow != 0)
            .map(|(i, _)| i)
            .enumerate()
            .map(|(i, n)| (n, i)),
    );

    let (states, nodes) = (state_nodes.len(), graph.len());

    let minutes = 30;

    let mut weights: Vec<usize> = vec![0; (1 << states) * nodes];
    let mut newweights: Vec<usize> = vec![0; (1 << states) * nodes];
    for min in 0..minutes {
        for (n, nw) in newweights.iter_mut().enumerate() {
            let (state, node) = (n / nodes, n % nodes);
            if state + 1 == 1 << states {
                continue;
            }
            for &dest in &graph[node].tunnels {
                *nw = max(*nw, weights[state * nodes + dest]);
            }
            if let Some(s) = state_nodes.get(&node) {
                if 1 << s & state == 0 {
                    *nw = max(
                        *nw,
                        weights[(state | 1 << s) * nodes + node] + min * graph[node].flow,
                    );
                }
            }
        }
        println!("{min}");
        std::mem::swap(&mut weights, &mut newweights);
    }
    let begin = graph.iter().position(|n| n.name == "AA").unwrap();
    println!("{:?}", weights[begin]);
    let minutes = 26;
    let packednodes = (nodes + 1) * nodes / 2;
    let num_to_state = |n: usize| {
        let (state, nodepair) = (n / packednodes, n % packednodes);
        let (node1, node2) = (nodepair / nodes, nodepair % nodes);
        if node1 > node2 {
            (state, nodes - node1, nodes - 1 - node2)
        } else {
            (state, node1, node2)
        }
    };
    let state_to_num = |state: usize, node1: usize, node2: usize| {
        let (node1, node2) = if node1 > node2 {
            (node2, node1)
        } else {
            (node1, node2)
        };
        let (node1, node2) = if node1 >= (nodes + 1) / 2 {
            (nodes - node1, nodes - 1 - node2)
        } else {
            (node1, node2)
        };
        state * packednodes + node1 * nodes + node2
    };

    let mut weights: Vec<usize> = vec![0; (1 << states) * packednodes];
    for min in 0..minutes {
        weights = (0..weights.len())
            .into_par_iter()
            .map(|n| {
                let (state, node1, node2) = num_to_state(n);
                if state + 1 == 1 << states || node2 < node1 {
                    return 0;
                }
                let mut maxval = 0;
                //for (n_state1, n_node1, n_weight1) in next_iter(node1, state) {
                for &dest1 in &graph[node1].tunnels {
                    for &dest2 in &graph[node2].tunnels {
                        maxval = max(maxval, weights[state_to_num(state, dest1, dest2)]);
                    }
                    if let Some(s2) = state_nodes.get(&node2) {
                        if 1 << s2 & state == 0 {
                            maxval = max(
                                maxval,
                                weights[state_to_num(1 << s2 | state, dest1, node2)]
                                    + min * graph[node2].flow,
                            );
                        }
                    }
                }
                if let Some(s1) = state_nodes.get(&node1) {
                    if 1 << s1 & state == 0 {
                        for &dest2 in &graph[node2].tunnels {
                            maxval = max(
                                maxval,
                                weights[state_to_num(1 << s1 | state, node1, dest2)]
                                    + min * graph[node1].flow,
                            );
                        }
                        if node1 != node2 {
                            if let Some(s2) = state_nodes.get(&node2) {
                                if 1 << s2 & state == 0 {
                                    maxval = max(
                                        maxval,
                                        weights
                                            [state_to_num(1 << s1 | 1 << s2 | state, node1, node2)]
                                            + min * (graph[node1].flow + graph[node2].flow),
                                    );
                                }
                            }
                        }
                    }
                }
                maxval
            })
            .collect();
        println!("{min}");
    }
    let begin = graph.iter().position(|n| n.name == "AA").unwrap();
    println!("{:?}", weights[state_to_num(0, begin, begin)]);
}
