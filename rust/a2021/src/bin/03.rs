fn main() {
    let mut bitdiff: Vec<i32> = vec![0; 32];
    for i in common::get_problem_lines(2021, 3) {
        for (i, c) in i.chars().rev().enumerate() {
            match c {
                '1' => bitdiff[i] += 1,
                '0' => bitdiff[i] -= 1,
                _ => panic!("invalid input"),
            }
        }
    }
    let (mut gamma, mut epsilon) = (0i32, 0i32);
    for (i, n) in bitdiff.iter().enumerate() {
        match 0.cmp(n) {
            std::cmp::Ordering::Less => gamma ^= 1 << i,
            std::cmp::Ordering::Greater => epsilon ^= 1 << i,
            std::cmp::Ordering::Equal => break,
        }
    }
    println!("part 1: {}", gamma * epsilon);

    let mut v: Vec<String> = common::get_problem_lines(2021, 3).collect();

    for i in 0..32 {
        let mut diff = 0;
        for s in v.iter() {
            match s.chars().nth(i) {
                Some('1') => diff += 1,
                Some('0') => diff -= 1,
                _ => panic!("invalid input"),
            }
        }
        if diff >= 0 {
            v.retain(|s| s.chars().nth(i) == Some('1'));
        } else {
            v.retain(|s| s.chars().nth(i) == Some('0'));
        }
        if v.len() == 1 {
            break;
        }
    }
    let o = i32::from_str_radix(&v[0], 2).unwrap();

    let mut v: Vec<String> = common::get_problem_lines(2021, 3).collect();
    for i in 0..32 {
        let mut diff = 0;
        for s in v.iter() {
            match s.chars().nth(i) {
                Some('1') => diff += 1,
                Some('0') => diff -= 1,
                _ => panic!("invalid input"),
            }
        }
        if diff >= 0 {
            v.retain(|s| s.chars().nth(i) == Some('0'));
        } else {
            v.retain(|s| s.chars().nth(i) == Some('1'));
        }
        if v.len() == 1 {
            break;
        }
    }
    let oo = i32::from_str_radix(&v[0], 2).unwrap();
    println!("part 2: {}", o * oo);
}
