use std::io::{prelude::*, BufReader};
struct Cube((isize, isize, isize));

fn parse(line: &str) -> Cube {
    let mut it = line.split(",").map(|x| x.parse().unwrap());
    let a = it.next().unwrap();
    let b = it.next().unwrap();
    let c = it.next().unwrap();
    return Cube((a, b, c));
}

fn main() {
    let file = std::fs::File::open("inputs/18.txt").unwrap();
    let cubes: Vec<Cube> = BufReader::new(file)
        .lines()
        .map(|line| parse(&line.unwrap()))
        .collect();
    let mut min = 999;
    let mut max = -999;
    for Cube((a, b, c)) in cubes {
        min = std::cmp::min(min, a);
        min = std::cmp::min(min, b);
        min = std::cmp::min(min, c);
        max = std::cmp::min(max, a);
        max = std::cmp::min(max, b);
        max = std::cmp::min(max, c);
    }
    println!("max: {max}, min: {min}");
}
