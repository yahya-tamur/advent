use std::io::{prelude::*, BufReader};

fn parse(line: &str) -> (usize, usize, usize) {
    let mut it = line.split(',').map(|x| x.parse().unwrap());
    let a: usize = it.next().unwrap();
    let b: usize = it.next().unwrap();
    let c: usize = it.next().unwrap();
    (a + 1, b + 1, c + 1)
}

fn main() {
    let file = std::fs::File::open("inputs/18.txt").unwrap();
    let cubes: Vec<(usize, usize, usize)> = BufReader::new(file)
        .lines()
        .map(|line| parse(&line.unwrap()))
        .collect();
    //cube indices range from 1 to 21 (after shifting in parse)
    let mut cubemap: Vec<i8> = vec![0; 22 * 22 * 22];

    let pack = |a, b, c| a * 22 * 22 + b * 22 + c;
    let edges = |a: usize, b: usize, c: usize| {
        [
            (a - 1, b, c),
            (a + 1, b, c),
            (a, b - 1, c),
            (a, b + 1, c),
            (a, b, c - 1),
            (a, b, c + 1),
        ]
    };

    for &(a, b, c) in cubes.iter() {
        cubemap[pack(a, b, c)] = 1;
    }

    let mut active_nodes: Vec<(usize, usize, usize)> = vec![(0, 0, 0)];
    while let Some((a, b, c)) = active_nodes.pop() {
        for (x, y, z) in edges(a, b, c) {
            if x > 21 || y > 21 || z > 21 {
                continue;
            }
            if cubemap[pack(x, y, z)] == 0 {
                active_nodes.push((x, y, z));
            }
        }
        cubemap[pack(a, b, c)] = 2;
    }

    let mut river_sides = 0;
    let mut air_sides = 0;

    for (a, b, c) in cubes {
        for (x, y, z) in edges(a, b, c) {
            match cubemap[pack(x, y, z)] {
                0 => air_sides += 1,
                2 => river_sides += 1,
                _ => (),
            }
        }
    }
    println!("part 1: {}", air_sides + river_sides);
    println!("part 2: {river_sides}");
}
