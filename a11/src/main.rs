use regex::Regex;
use std::fs;

struct Monkey {
    items: Vec<u64>,
    operation: Box<dyn Fn(u64) -> u64>,
    testdiv: u64,
    t_monkey: usize,
    f_monkey: usize,
}

fn parse_monkey(s: &str) -> Monkey {
    let r = Regex::new(
        r"(?x)
    .*\n
    .*items:\ (?P<nums>(\d+(,\ )?)+)\n
    .*new\ =\ (?P<op_left>old|\d+)\ (?P<op>\*|\+)\ (?P<op_right>old|\d+)\n
    .*divisible\ by\ (?P<testdiv>\d+)\n
    .*true.*monkey\ (?P<t_monkey>\d+)\n
    .*false.*monkey\ (?P<f_monkey>\d+)\n
    ",
    )
    .unwrap();
    let caps = r.captures(s).unwrap();
    let left = match caps.name("op_left").unwrap().as_str() {
        "old" => None,
        num => Some(num.parse().unwrap()),
    };
    let right = match caps.name("op_right").unwrap().as_str() {
        "old" => None,
        num => Some(num.parse().unwrap()),
    };
    let op_is_mult = caps.name("op").unwrap().as_str() == "*";

    Monkey {
        items: caps
            .name("nums")
            .unwrap()
            .as_str()
            .split(", ")
            .map(|x| x.parse::<u64>().unwrap())
            .collect::<Vec<u64>>(),
        operation: Box::new(move |x| {
            let l = if let Some(l) = left { l } else { x };
            let r = if let Some(r) = right { r } else { x };
            if op_is_mult {
                l * r
            } else {
                l + r
            }
        }),
        testdiv: caps.name("testdiv").unwrap().as_str().parse().unwrap(),
        t_monkey: caps.name("t_monkey").unwrap().as_str().parse().unwrap(),
        f_monkey: caps.name("f_monkey").unwrap().as_str().parse().unwrap(),
    }
}

const ROUNDS: usize = 10000;

fn main() {
    let s: String = fs::read_to_string("input.txt").unwrap();
    let mut it = s.split("Monkey");
    it.next();
    let monkeys: Vec<Monkey> = it.map(parse_monkey).collect();
    let mut monkey_items: Vec<Vec<u64>> = monkeys.iter().map(|m| m.items.clone()).collect();
    let mut monkey_counts = vec![0u64; monkeys.len()];
    let mmmm: u64 = monkeys.iter().map(|m| m.testdiv).product();

    for _ in 0..ROUNDS {
        for (n, mon) in monkeys.iter().enumerate() {
            let mut v: Vec<u64> = vec![];
            std::mem::swap(&mut v, &mut monkey_items[n]);
            for i in v {
                monkey_counts[n] += 1;
                let i = (mon.operation)(i);
                //uncomment for part 1: let i = i / 3;
                if (i / mon.testdiv) * mon.testdiv == i {
                    monkey_items[mon.t_monkey].push(i % mmmm);
                } else {
                    monkey_items[mon.f_monkey].push(i % mmmm);
                }
            }
        }
    }
    for (i, n) in monkey_counts.iter().enumerate() {
        println!("Monkey {i} inspected {n} times");
    }
    monkey_counts.sort();
    let l = monkey_counts.len();
    println!(
        "monkey business: {}",
        monkey_counts[l - 1] * monkey_counts[l - 2]
    );
}
