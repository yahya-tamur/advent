use regex::Regex;
use std::fs::File;
use std::io::{prelude::*, BufReader};

fn parse_line(s: &str) -> Option<(i32, i32, i32, i32)> {
    let r = Regex::new(r"(\d+)-(\d+),(\d+)-(\d+)").unwrap();
    let caps = r.captures(s)?;
    Some((
        caps.get(1)?.as_str().parse().ok()?,
        caps.get(2)?.as_str().parse().ok()?,
        caps.get(3)?.as_str().parse().ok()?,
        caps.get(4)?.as_str().parse().ok()?,
    ))
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);

    let mut sum = 0;
    let mut sum2 = 0;
    for line in reader.lines().map(|a| a.unwrap()) {
        let (a, b, c, d) = parse_line(&line).unwrap();
        if (c <= a && b <= d) || (a <= c && d <= b) {
            sum += 1;
        }
        if (c <= b) && (a <= d) {
            sum2 += 1;
        }
    }
    println!("{} {}", sum, sum2);
    Ok(())
}
