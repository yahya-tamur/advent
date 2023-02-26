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

const MINUTES: usize = 26;

fn main() {
    let s = std::fs::read_to_string("input.txt").unwrap();
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
    let num_to_state = |n: usize| (n / nodes / nodes, (n % (nodes * nodes)) / nodes, n % nodes);
    let state_to_num =
        |state: usize, node1: usize, node2: usize| (state * nodes * nodes + node1 * nodes + node2);

    let next_iter = |node: usize, state: usize| {
        let i = graph[node].tunnels.iter().map(move |dest| (0, *dest, 0));
        if let Some(s) = state_nodes.get(&node) {
            if 1 << s & state == 0 {
                return i.chain(std::iter::once((1 << s, node, graph[node].flow)));
            }
        }
        i.chain(std::iter::once((usize::MAX, 0, 0)))
    };

    let mut weights: Vec<usize> = vec![0; (1 << states) * nodes * nodes];
    for min in 0..MINUTES {
        weights = (0..weights.len())
            .into_par_iter()
            .map(|n| {
                let (state, node1, node2) = num_to_state(n);
                if state + 1 == 1 << states {
                    return 0;
                }
                let mut maxval = 0;
                for (n_state1, n_node1, n_weight1) in next_iter(node1, state) {
                    for (n_state2, n_node2, n_weight2) in next_iter(node2, state) {
                        if n_state1 != usize::MAX
                            && n_state2 != usize::MAX
                            && ((n_state1 == 0 && n_state2 == 0) || n_state1 != n_state2)
                        {
                            maxval = max(
                                maxval,
                                weights
                                    [state_to_num(n_state1 | n_state2 | state, n_node1, n_node2)]
                                    + min * (n_weight1 + n_weight2),
                            );
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
