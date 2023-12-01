use regex::{Match, Regex};

fn parse() -> Vec<(i32, i32, i32, i32)> {
    let re = Regex::new(r"(?P<a>\d+),(?P<b>\d+) -> (?P<c>\d+),(?P<d>\d+)").unwrap();
    let read = |c: Option<Match>| c.unwrap().as_str().parse().unwrap();
    re.captures_iter(&common::get_problem(2021, 5))
        .map(|cap| {
            (
                read(cap.name("a")),
                read(cap.name("b")),
                read(cap.name("c")),
                read(cap.name("d")),
            )
        })
        .collect()
}

use std::cmp::Ordering;
fn boardmatch(lines: Vec<(i32, i32, i32, i32)>, part1: bool) -> i32 {
    let mut board = vec![vec![0; 1000]; 1000];
    let sgn = |z: i32| match z.cmp(&0) {
        Ordering::Less => -1,
        Ordering::Equal => 0,
        Ordering::Greater => 1,
    };
    for (x1, y1, x2, y2) in lines {
        if part1 && (x1 != x2) && (y1 != y2) {
            continue;
        }
        let (d1, d2) = (sgn(x2 - x1), sgn(y2 - y1));
        let (mut i, mut j) = (x1, y1);
        while (i != x2) || (j != y2) {
            board[i as usize][j as usize] += 1;
            i += d1;
            j += d2;
        }
        board[x2 as usize][y2 as usize] += 1;
    }
    let mut ans = 0;
    for row in board {
        for val in row {
            if val > 1 {
                ans += 1;
            }
        }
    }
    ans
}

fn main() {
    println!("part 1: {}", boardmatch(parse(), true));
    println!("part 2: {}", boardmatch(parse(), false));
}
