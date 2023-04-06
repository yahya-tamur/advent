//let's say left to right is actually least to most significant bit
type Snafu = Vec<i8>;

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
        match n.rem_euclid(5) {
            a @ (0 | 1 | 2) => {
                ans.push(a as i8);
                n -= a;
            }
            a @ (3 | 4) => {
                let a = a - 5;
                ans.push(a as i8);
                n -= a;
            }
            _ => panic!(),
        }
        assert!(n % 5 == 0);
        n /= 5;
    }

    ans
}

fn main() {
    let input = std::fs::read_to_string("inputs/25.txt").unwrap();
    let mut ans = 0;
    for line in input.lines() {
        ans += to_int(&parse_snafu(line));
    }
    println!("{}", encode_snafu(&to_snafu(ans)));
}
