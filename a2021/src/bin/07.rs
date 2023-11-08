fn part1(v: &Vec<i64>) -> i64 {
    //i don't know if this would work for other arrays -- here,
    //n = 1000, v[n/2] = v[(n/2)+1].
    let n = v.len();
    let m = if (n & 1) == 0 {
        //even
        (v[n / 2] + v[(n / 2) + 1]) / 2
    } else {
        v[n / 2]
    };
    let mut ans = 0;
    for &n in v {
        if n > m {
            ans += n - m
        } else {
            ans += m - n
        }
    }
    ans
}

fn part2(v: &Vec<i64>) -> i64 {
    let mut minval = i64::MAX;
    for i in v[0]..=v[v.len() - 1] {
        let mut val = 0;
        for &vv in v {
            let diff = if i > vv { i - vv } else { vv - i };
            val += diff * (diff + 1) / 2
        }
        if val < minval {
            minval = val;
        }
    }
    minval
}

fn main() {
    let mut nums: Vec<i64> = common::get_problem_lines(2021, 7)
        .next()
        .unwrap()
        .split(',')
        .map(|s| s.parse::<i64>().unwrap())
        .collect();
    nums.sort();
    println!("{:#?}", part1(&nums));
    println!("{:#?}", part2(&nums));
}
