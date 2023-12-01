use regex::Regex;
use Instr::*;

enum Instr {
    Forward(i32),
    Up(i32),
    Down(i32),
}

fn parse(s: &str) -> Vec<Instr> {
    let r = Regex::new(r"(?x)((?P<f>forward\ )|(?P<d>down\ )|(?P<u>up\ ))(?P<n>\d+)").unwrap();
    r.captures_iter(s)
        .map(|caps| {
            let amount: i32 = caps.name("n").unwrap().as_str().parse().unwrap();
            match () {
                () if caps.name("f").is_some() => Forward(amount),
                () if caps.name("d").is_some() => Down(amount),
                () if caps.name("u").is_some() => Up(amount),
                _ => panic!("invald input"),
            }
        })
        .collect()
}

fn main() {
    let (h, d) = parse(&common::get_problem(2021, 2))
        .into_iter()
        .fold((0, 0), |(h, d), instr| match instr {
            Forward(n) => (h + n, d),
            Up(n) => (h, d - n),
            Down(n) => (h, d + n),
        });
    println!("part1: {}", h * d);
    let (_, h, d) =
        parse(&common::get_problem(2021, 2))
            .into_iter()
            .fold((0, 0, 0), |(aim, h, d), instr| match instr {
                Forward(n) => (aim, h + n, d + aim * n),
                Up(n) => (aim - n, h, d),
                Down(n) => (aim + n, h, d),
            });
    println!("part2: {}", h * d);
}
