fn get_m() -> Vec<Vec<i64>> {
    vec![
        vec![0, 1, 0, 0, 0, 0, 0, 0, 0],
        vec![0, 0, 1, 0, 0, 0, 0, 0, 0],
        vec![0, 0, 0, 1, 0, 0, 0, 0, 0],
        vec![0, 0, 0, 0, 1, 0, 0, 0, 0],
        vec![0, 0, 0, 0, 0, 1, 0, 0, 0],
        vec![0, 0, 0, 0, 0, 0, 1, 0, 0],
        vec![1, 0, 0, 0, 0, 0, 0, 1, 0],
        vec![0, 0, 0, 0, 0, 0, 0, 0, 1],
        vec![1, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
}

fn times(a: &[Vec<i64>], b: &[Vec<i64>]) -> Vec<Vec<i64>> {
    let p = b[0].len();
    let mut ans = vec![vec![0; p]; a.len()];
    for (i, ai) in a.iter().enumerate() {
        for (j, bj) in b.iter().enumerate() {
            for (k, bjk) in bj.iter().enumerate() {
                ans[i][k] += ai[j] * bjk;
            }
        }
    }
    ans
}

fn mnv(mut m: Vec<Vec<i64>>, mut n: u16, mut v: Vec<Vec<i64>>) -> Vec<Vec<i64>> {
    while n != 0 {
        if (n & 1) != 0 {
            v = times(&m, &v);
        }
        n >>= 1;
        m = times(&m, &m);
    }
    v
}

fn iterate(i: u16) -> i64 {
    let mut timers = vec![vec![0]; 9];
    for num in common::get_problem_lines(2021, 6)
        .next()
        .unwrap()
        .split(',')
        .map(|s| s.parse::<i64>().unwrap())
    {
        timers[num as usize][0] += 1;
    }
    let ans = mnv(get_m(), i, timers);

    ans[0][0]
        + ans[1][0]
        + ans[2][0]
        + ans[3][0]
        + ans[4][0]
        + ans[5][0]
        + ans[6][0]
        + ans[7][0]
        + ans[8][0]
}

fn main() {
    println!("part 1: {}", iterate(80));
    println!("part 2: {}", iterate(256));
}
