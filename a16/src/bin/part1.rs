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

const MINUTES: usize = 30;

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

    let mut weights: Vec<usize> = vec![0; (1 << states) * nodes];
    let mut newweights: Vec<usize> = vec![0; (1 << states) * nodes];
    for min in 0..MINUTES {
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
}
