use regex::Regex;
use std::cmp::max;

fn parse_line(s: &str) -> Vec<(usize, usize)> {
    let r = Regex::new(r"(?P<first>\d+),(?P<second>\d+)").unwrap();

    r.captures_iter(s)
        .map(|caps| {
            (
                caps.name("first").unwrap().as_str().parse().unwrap(),
                caps.name("second").unwrap().as_str().parse().unwrap(),
            )
        })
        .collect()
}

const ROWS: usize = 1000;
const COLS: usize = 200;

fn main() {
    let mut spots = vec![vec![false; COLS]; ROWS];
    let mut maxy = 0;
    for line in common::get_problem_lines(2022, 14) {
        let v = parse_line(&line);
        maxy = max(maxy, v.iter().map(|(_, y)| *y).max().unwrap_or(0));
        for i in 1..v.len() {
            if v[i - 1].0 == v[i].0 {
                for t in if v[i - 1].1 < v[i].1 {
                    v[i - 1].1..=v[i].1
                } else {
                    v[i].1..=v[i - 1].1
                } {
                    spots[v[i].0][t] = true;
                }
            } else {
                for t in if v[i - 1].0 < v[i].0 {
                    v[i - 1].0..=v[i].0
                } else {
                    v[i].0..=v[i - 1].0
                } {
                    spots[t][v[i].1] = true;
                }
            }
        }
    }

    //make floor. comment these three lines for part 1.
    /**/
    for row in &mut spots {
        row[maxy + 2] = true;
    }
    // */
    let mut sands = 0;
    'pileup: loop {
        let (mut sandx, mut sandy) = (500, 0);
        'flow: loop {
            if spots[500][0] {
                break 'pileup;
            }
            if sandy + 1 == COLS {
                break 'pileup;
            }
            if !spots[sandx][sandy + 1] {
                sandy += 1;
                continue 'flow;
            }
            if !spots[sandx - 1][sandy + 1] {
                sandx -= 1;
                sandy += 1;
                continue 'flow;
            }
            if !spots[sandx + 1][sandy + 1] {
                sandx += 1;
                sandy += 1;
                continue 'flow;
            }
            spots[sandx][sandy] = true;
            sands += 1;
            break 'flow;
        }
    }

    /*
    for row in spots.iter().take(600).skip(400) {
        for &el in row.iter().take(200) {
            if el {
                print!("#");
            } else {
                print!(" ");
            }
        }
        println!();
    }
    */

    println!("{}", sands);
}
