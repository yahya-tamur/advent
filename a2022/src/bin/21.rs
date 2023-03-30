//HashMap does make tree operations slightly slower probably but is closer to
//the input.
//
//otherwise very straightforward implementation:
//
// * propogate constants except humn
// * getx(tree, node, eq) recursively traverses tree with one x and
// * finds value of x that makes node eq to get part 2 answer
//
// * finish propagating contants to get part 1 answer
//
// I'm happy I managed to use all &str's and no string copies
use regex::Regex;
use std::collections::HashMap;

#[derive(Debug, Clone, Copy)]
enum Op {
    Add,
    Sub,
    Mul,
    Div,
}

#[derive(Debug)]
enum Node<'a> {
    Num(i64),
    X(i64),
    Binop(&'a str, &'a str, Op),
}

fn parse(s: &str) -> HashMap<&str, Node<'_>> {
    let r = Regex::new(
        r"(?xm)^
        (?P<name>[[:alpha:]]{4}):\ 
        ((?P<num>\d+)|
         (?P<left>[[:alpha:]]{4})\ (?P<op>.)\ (?P<right>[[:alpha:]]{4}))$
        ",
    )
    .unwrap();
    r.captures_iter(s)
        .map(|caps| {
            let name = caps.name("name").unwrap().as_str();
            (
                name,
                if let Some(numcap) = caps.name("num") {
                    let x = numcap.as_str().parse().unwrap();
                    if name == "humn" {
                        Node::X(x)
                    } else {
                        Node::Num(x)
                    }
                } else {
                    Node::Binop(
                        caps.name("left").unwrap().as_str(),
                        caps.name("right").unwrap().as_str(),
                        match caps.name("op").unwrap().as_str() {
                            "+" => Op::Add,
                            "-" => Op::Sub,
                            "*" => Op::Mul,
                            "/" => Op::Div,
                            _ => panic!("unknown operator"),
                        },
                    )
                },
            )
        })
        .collect()
}

fn const_prop<'a>(
    hm: &mut HashMap<&'a str, Node<'a>>,
    search: &'a str,
    part1: bool,
) -> Option<i64> {
    match *hm.get(search).unwrap() {
        Node::Binop(left, right, op) => {
            if let (Some(l), Some(r)) = (const_prop(hm, left, part1), const_prop(hm, right, part1))
            {
                let i = match op {
                    Op::Add => l + r,
                    Op::Sub => l - r,
                    Op::Mul => l * r,
                    Op::Div => l / r,
                };
                hm.insert(search, Node::Num(i));
                Some(i)
            } else {
                None
            }
        }
        Node::Num(n) => Some(n),
        Node::X(n) => {
            if part1 {
                Some(n)
            } else {
                None
            }
        }
    }
}

fn getx<'a>(hm: &HashMap<&'a str, Node<'a>>, node: &'a str, eq: i64) -> i64 {
    match hm.get(node).unwrap() {
        Node::Binop(left, right, op) => match (hm.get(left).unwrap(), hm.get(right).unwrap()) {
            (_, Node::Num(r)) => getx(
                hm,
                left,
                match op {
                    Op::Add => eq - r,
                    Op::Sub => eq + r,
                    Op::Mul => eq / r,
                    Op::Div => eq * r,
                },
            ),
            (Node::Num(l), _) => getx(
                hm,
                right,
                match op {
                    Op::Add => eq - l,
                    Op::Sub => l - eq,
                    Op::Mul => eq / l,
                    Op::Div => l / eq,
                },
            ),
            _ => panic!("binop with neither end nums"),
        },
        Node::X(_) => eq,
        Node::Num(_) => panic!("got a constant on getx"),
    }
}

fn main() {
    let file = std::fs::read_to_string("inputs/21.txt").unwrap();
    let mut hm = parse(&file);

    const_prop(&mut hm, "root", false);
    let (left, right) = match hm.get("root").unwrap() {
        Node::Binop(left, right, _) => (left, right),
        _ => panic!(""),
    };
    let part2ans = match (hm.get(left).unwrap(), hm.get(right).unwrap()) {
        (Node::Num(l), _) => getx(&hm, right, *l),
        (_, Node::Num(r)) => getx(&hm, left, *r),
        _ => panic!(""),
    };

    println!("part 1: {:?}", const_prop(&mut hm, "root", true).unwrap());
    println!("part 2: {}", part2ans);
}
