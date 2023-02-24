//T - status
//(-1,0,1) ^2
//
//t-visited: bool array

use regex::Regex;
use std::fs::File;
use std::io::{prelude::*, BufReader};

//up: (0,1), right: (0,1)
fn parse_line(s: &str) -> Vec<(i32, i32)> {
    let r = Regex::new(r"(?P<dir>R|L|U|D) (?P<num>\d+)").unwrap();
    let caps = r.captures(s).unwrap();
    let num: usize = caps.name("num").unwrap().as_str().parse().unwrap();
    vec![
        match caps.name("dir").unwrap().as_str() {
            "D" => (0, -1),
            "U" => (0, 1),
            "L" => (-1, 0),
            "R" => (1, 0),
            _ => panic!("invalid input"),
        };
        num
    ]
}

const START: usize = 150;
const MAX: usize = 500;
const ROPE_LEN: usize = 10; //set to 2 for part 1

fn main() {
    let mut rope: Vec<(i32, i32)> = vec![(START as i32, START as i32); ROPE_LEN];
    let mut spots: Vec<Vec<bool>> = vec![vec![false; MAX]; MAX];
    let (hx, hy) = rope[0];
    spots[hx as usize][hy as usize] = true;

    let file = File::open("input.txt").unwrap();
    for line in BufReader::new(file).lines().map(|x| x.unwrap()) {
        for (dx, dy) in parse_line(&line) {
            let (hx, hy) = rope[0];
            rope[0] = (hx + dx, hy + dy);
            for i in 0..(ROPE_LEN - 1) {
                let (hx, hy) = rope[i];
                let (tx, ty) = rope[i + 1];
                let (dxs, dys) = ((hx - tx) * (hx - tx), (hy - ty) * (hy - ty));
                rope[i + 1] = match () {
                    () if dxs == 4 && dys == 4 => ((hx + tx) / 2, (ty + hy) / 2),
                    () if dys == 4 => (hx, (ty + hy) / 2),
                    () if dxs == 4 => ((hx + tx) / 2, hy),
                    _ => (tx, ty),
                }
            }
            let (tx, ty) = rope[ROPE_LEN - 1];
            spots[tx as usize][ty as usize] = true;
        }
    }

    println!(
        "{:?}",
        spots
            .iter()
            .map(|bs| bs.iter().map(|&b| b as i32).sum::<i32>())
            .sum::<i32>()
    );
}
