use regex::Regex;
use std::collections::VecDeque;

fn parse_move(s: &str) -> Option<(usize, usize, usize)> {
    let r = Regex::new(r"move (\d+) from (\d+) to (\d+)").unwrap();
    let caps = r.captures(s)?;
    let a: usize = caps.get(1)?.as_str().parse().ok()?;
    let b: usize = caps.get(2)?.as_str().parse().ok()?;
    let c: usize = caps.get(3)?.as_str().parse().ok()?;
    Some((a, b - 1, c - 1))
}

const MAX_HEIGHT: usize = 8;
const NUM_BOXES: usize = 9;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut it = common::get_problem_lines(2022, 5);
    let mut boxes: Vec<VecDeque<u8>> = vec![VecDeque::new(); NUM_BOXES];

    for _ in 0..MAX_HEIGHT {
        let line = it.next().unwrap();
        let line = line.as_bytes();
        for i in 0..NUM_BOXES {
            let b = line[4 * i + 1];
            if b != 32 {
                boxes[i].push_back(b);
            }
        }
    }
    it.next();
    it.next();
    for line in it {
        let (n, src, dest) = parse_move(&line).unwrap();
        //swap between these sections for parts 1 and 2
        /*
        for _ in 0..n {
            let c = boxes[src].pop_front().unwrap();
            boxes[dest].push_front(c);
        }
        // */
        /**/
        let mut split_end = boxes[src].split_off(n);
        std::mem::swap(&mut boxes[src], &mut split_end);
        std::mem::swap(&mut boxes[dest], &mut split_end);
        boxes[dest].append(&mut split_end);
        // */
    }
    for bo in &boxes {
        print!("{}", *bo.front().unwrap() as char);
    }
    println!();
    Ok(())
}
