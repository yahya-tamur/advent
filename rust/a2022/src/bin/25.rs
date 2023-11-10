//let's say left to right is actually least to most significant bit
type Snafu = Vec<i8>;
use common::get_problem_lines;

fn parse_snafu(v: &str) -> Snafu {
    v.chars()
        .map(|c| match c {
            '2' => 2,
            '1' => 1,
            '0' => 0,
            '-' => -1,
            '=' => -2,
            _ => panic!("unrecognized expression"),
        })
        .rev()
        .collect()
}

fn encode_snafu(v: &Snafu) -> String {
    v.iter()
        .map(|i| match i {
            2 => '2',
            1 => '1',
            0 => '0',
            -1 => '-',
            -2 => '=',
            _ => panic!("invalid snafu"),
        })
        .rev()
        .collect()
}

fn to_int(v: &Snafu) -> i128 {
    let mut ans: i128 = 0;
    for i in v.iter().rev() {
        ans *= 5;
        ans += *i as i128;
    }
    ans
}

fn to_snafu(mut n: i128) -> Snafu {
    let mut ans = vec![];
    while n != 0 {
        let a = match n.rem_euclid(5) {
            a @ (0 | 1 | 2) => a,
            a @ (3 | 4) => a - 5,
            _ => panic!("rem euclid returned something else???"),
        };
        ans.push(a as i8);
        n -= a;
        assert!(n % 5 == 0);
        n /= 5;
    }
    ans
}

fn main() {
    println!(
        "{}",
        encode_snafu(&to_snafu(
            get_problem_lines(2022, 25)
                .map(|line| to_int(&parse_snafu(&line)))
                .sum()
        ))
    )
}
