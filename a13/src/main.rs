use regex::Regex;
use std::cmp::Ordering;
use std::fs::File;
use std::io::{prelude::*, BufReader};
use std::iter::zip;

#[derive(Debug)]
enum Com {
    MoveIn,
    MoveOut,
    Num(i32),
    Noop,
}

#[derive(Debug, PartialEq, Eq)]
enum Tree {
    Num(i32),
    List(Vec<Tree>),
}

impl PartialOrd for Tree {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

use crate::Tree::{List, Num};

impl Ord for Tree {
    fn cmp(&self, other: &Self) -> Ordering {
        match (self, other) {
            (Num(n), Num(m)) => n.cmp(m),
            (List(v), List(w)) => zip(v, w)
                .fold(Ordering::Equal, |o, (vv, ww)| o.then(vv.cmp(ww)))
                .then(v.len().cmp(&w.len())),
            (Num(n), t) => List(vec![Num(*n)]).cmp(t),
            (t, Num(n)) => t.cmp(&List(vec![Num(*n)])),
        }
    }
}

fn make_tree(v: Vec<Com>) -> Tree {
    let mut heads: Vec<Tree> = vec![List(vec![])];
    for com in v {
        match com {
            Com::MoveIn => {
                heads.push(List(vec![]));
            }
            Com::MoveOut => {
                let t = heads.pop().unwrap();
                if let List(l) = heads.last_mut().unwrap() {
                    l.push(t);
                }
            }
            Com::Num(n) => {
                if let List(l) = heads.last_mut().unwrap() {
                    l.push(Num(n));
                }
            }
            Com::Noop => {}
        }
        //println!("{:?}", heads);
    }
    if let List(mut l) = heads.pop().unwrap() {
        l.pop().unwrap()
    } else {
        panic!("too many closing braces!")
    }
}

fn parse_line(s: &str) -> Vec<Com> {
    let r = Regex::new(
        r"(?x)
    (?P<left>\[)|
    (?P<right>\])|
    (?P<num>\d+)|
    (?P<ced>,)
    ",
    )
    .unwrap();
    r.captures_iter(s)
        .map(|caps| match () {
            () if caps.name("left").is_some() => Com::MoveIn,
            () if caps.name("right").is_some() => Com::MoveOut,
            () if caps.name("ced").is_some() => Com::Noop,
            _ => Com::Num(caps.name("num").unwrap().as_str().parse().unwrap()),
        })
        .collect()
}

fn mtpl(s: &str) -> Tree {
    make_tree(parse_line(s))
}

fn main() {
    let file = File::open("input.txt").unwrap();

    /**/
    let it = BufReader::new(file).lines();

    let mut trees = vec![mtpl("[[2]]"), mtpl("[[6]]")];
    for line in it.map(|x| x.unwrap()) {
      if line != "" {
        trees.push(mtpl(&line));
      }
    }
    trees.sort();
    let l = trees.binary_search(&mtpl("[[2]]")).unwrap();
    let r = trees.binary_search(&mtpl("[[6]]")).unwrap();
    println!("decoder key: {:?}", (l+1)*(r+1));
    // */

    /*
    let mut it = BufReader::new(file).lines();
    let mut sum = 0;
    let mut pairs = 1;
    loop {
        let left = mtpl(&it.next().unwrap().unwrap());
        let right = mtpl(&it.next().unwrap().unwrap());
        if left < right {
            sum += pairs;
        }
        pairs += 1;
        if it.next().is_none() {
            break;
        }
    }
    println!("{sum}");
    // */
}
