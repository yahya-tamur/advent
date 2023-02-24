use regex::Regex;
use std::fs::File;
use std::io::{prelude::*, BufReader};

//returns (cycles to wait, value to add after)
fn parse_line(s: &str) -> (i32, i32) {
    let r = Regex::new(
        r"(?x)
      (?P<noop>noop)|
      (?P<addx>addx\ (?P<num>-?\d+))",
    )
    .unwrap();
    let caps = r.captures(s).unwrap();
    match () {
        () if caps.name("noop").is_some() => (1, 0),
        () if caps.name("addx").is_some() => (
            2,
            caps.name("num").unwrap().as_str().parse::<i32>().unwrap(),
        ),
        _ => panic!("invalid input"),
    }
}

fn main() {
    let file = File::open("input.txt").unwrap();
    let mut it = BufReader::new(file).lines().map(|x| x.unwrap());
    let mut x = 1;
    let (mut wait, mut newval) = parse_line(&it.next().unwrap());
    let mut sum = 0;
    println!();
    for cycle in 1..250 {
        match cycle {
            20 | 60 | 100 | 140 | 180 | 220 => {
                //println!("{x}");
                sum += cycle * x;
            }
            _ => {}
        };
        if cycle != 0 {
            if x - 1 <= ((cycle - 1) % 40) && ((cycle - 1) % 40) <= x + 1 {
                print!("#");
            } else {
                print!(".");
            }
        }
        match cycle {
            40 | 80 | 120 | 160 | 200 | 240 => {
                println!();
            }
            _ => {}
        }
        wait -= 1;
        if wait == 0 {
            x += newval;
            match it.next() {
                Some(s) => {
                    (wait, newval) = parse_line(&s);
                }
                None => {
                    break;
                }
            }
        }
    }
    println!("{sum}");
}
