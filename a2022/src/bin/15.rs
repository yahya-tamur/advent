use regex::Regex;
use std::cmp::{max, min};
use std::fs;

fn parse_lines(s: &str) -> Vec<(i64, i64, i64, i64)> {
    let r = Regex::new(
        r"(?x).*x=(?P<x1>-?\d+).*y=(?P<y1>-?\d+)
    .*x=(?P<x2>-?\d+).*y=(?P<y2>-?\d+)\n",
    )
    .unwrap();

    r.captures_iter(s)
        .map(|caps| {
            (
                caps.name("x1").unwrap().as_str().parse().unwrap(),
                caps.name("y1").unwrap().as_str().parse().unwrap(),
                caps.name("x2").unwrap().as_str().parse().unwrap(),
                caps.name("y2").unwrap().as_str().parse().unwrap(),
            )
        })
        .collect()
}

//const SCANLINE: i64 = 2000000;
const MAXSCAN: i64 = 4000000;

//intervals are inclusive.
fn beacon_to_interval(x1: i64, y1: i64, x2: i64, y2: i64, scan: i64) -> (i64, i64) {
    let d = (x1 - x2).abs() + (y1 - y2).abs() - (y1 - scan).abs();
    (x1 - d, x1 + d)
}

fn main() {
    let input = fs::read_to_string("inputs/15.txt").unwrap();
    let beacons = parse_lines(&input);

    let mut line = 0;
    loop {
        let mut intervals: Vec<(i64, i64)> = beacons
            .iter()
            .map(|x| beacon_to_interval(x.0, x.1, x.2, x.3, line))
            .filter(|(x, y)| x <= y)
            .collect();
        intervals.sort();
        let mut min_overlap = 10;
        let ans: Vec<(i64, i64)> = intervals
            .into_iter()
            .map(|x| vec![x])
            .reduce(|mut v, w| {
                let n = v.len() - 1;
                let (vi, vj) = v[n];
                let (wi, wj) = w[0];
                if vj >= wi - 1 {
                    min_overlap = min(vj - wi, min_overlap);
                    v[n] = (vi, max(vj, wj));
                } else {
                    v.push((wi, wj));
                }
                v
            })
            .unwrap();
        //println!("{}", line);
        if ans.len() != 1 || line >= MAXSCAN {
            println!("{} {:?}", line, ans);
            let (x, y) = (line, ans[0].1 + 1);
            println!("{}", 4000000 * y + x);
            break;
        }
        line += if min_overlap == 0 { 1 } else { min_overlap };
    }
}
