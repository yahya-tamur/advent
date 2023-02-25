use regex::Regex;
use std::fs::File;
use std::io::{prelude::*, BufReader};

#[derive(Debug)]
enum Com<'a> {
    MoveIn(&'a str),
    MoveOut,
    Add(i32),
    Noop,
}

fn parse_line(s: &str) -> Option<Com> {
    let r = Regex::new(
        r"(?x)
    (?P<out>\$\ cd\ \.\.)|
    (?P<in>\$\ cd\ (?P<dirname>[/[:alpha:]]+))|
    (?P<dir>dir\ [[:alpha:]]+)|
    (?P<ls>\$\ ls)|
    (?P<file>(?P<filesize>\d+)\ [.[:alpha:]])
    ",
    )
    .unwrap();
    let caps = r.captures(s).unwrap();
    match () {
        () if caps.name("out").is_some() => Some(Com::MoveOut),
        () if caps.name("in").is_some() => {
            Some(Com::MoveIn(caps.name("dirname").unwrap().as_str()))
        }
        () if caps.name("ls").is_some() => Some(Com::Noop),
        () if caps.name("dir").is_some() => Some(Com::Noop),
        () if caps.name("file").is_some() => Some(Com::Add(
            caps.name("filesize").unwrap().as_str().parse().unwrap(),
        )),
        _ => None,
    }
}

// found in another run
const ALL_SIZE: i32 = 41072511;

fn main() {
    let file = File::open("input.txt").unwrap();
    let it = BufReader::new(file).lines();
    let mut sum = 0;
    let mut bestdir: (String, i32) = ("none yet!".to_string(), i32::MAX);

    let mut stack = Vec::<(String, i32)>::new();

    let add = |stack: &mut Vec<(String, i32)>, n: i32| {
        let i = stack.len() - 1;
        let (s, k) = &stack[i];
        stack[i] = (s.to_string(), k + n);
    };

    let mut moveout = |stack: &mut Vec<(String, i32)>| {
        let (name, d_size) = stack.pop().unwrap();
        if d_size < bestdir.1 && ALL_SIZE - d_size <= 40000000 {
            bestdir.0 = name;
            bestdir.1 = d_size;
        }
        if d_size <= 100000 {
            sum += d_size;
        }
        if !stack.is_empty() {
            add(stack, d_size);
        }
    };
    for line in it.map(|x| x.unwrap()) {
        match parse_line(&line).unwrap() {
            Com::MoveOut => {
                moveout(&mut stack);
            }
            Com::MoveIn(s) => {
                stack.push((s.to_string(), 0));
            }
            Com::Add(n) => {
                add(&mut stack, n);
            }
            Com::Noop => {}
        };
    }
    while !stack.is_empty() {
        moveout(&mut stack);
    }
    println!("sum: {}", sum);
    println!("bestdir: {:?}", bestdir);
}
