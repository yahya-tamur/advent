//is there a non-quadratic solution to this?
//I think for part 1, my solution is faster than
//keeping an actual list and shifting, but only
//by a constant factor.
//
//it's definitely too slow in part 2, since
//lambdas accumulate as we mix 10 times.
//
//maybe the naive solution would be slow too?
//
//I wonder how programs like GAP implement
//elements of the symmetric group, since that's
//essentially what 'lambdas' is or the linked
//list would be.

struct State {
    lambdas: Vec<(i64, i64)>,
    length: i64,
}

impl State {
    fn new(length: i64) -> Self {
        State {
            lambdas: Vec::new(),
            length,
        }
    }

    fn add_lambda(&mut self, start: i64, end: i64) {
        self.lambdas.push((start, end));
    }

    fn apply(&self, mut i: i64) -> i64 {
        for &(start, delta) in self.lambdas.iter() {
            let end = (start + delta).rem_euclid(self.length - 1);
            if i == start {
                i = end
            } else if end <= i && i < start {
                i += 1
            } else if start < i && i <= end {
                i -= 1
            }
        }
        i
    }

    fn reverse_apply(&self, mut i: i64) -> i64 {
        for &(start, delta) in self.lambdas.iter().rev() {
            let end = (start + delta).rem_euclid(self.length - 1);
            if i == end {
                i = start
            } else if end < i && i <= start {
                i -= 1
            } else if start <= i && i < end {
                i += 1
            }
        }
        i
    }
}

fn get_ans(v: &Vec<i64>, n: usize) -> i64 {
    let mut s = State::new(v.len() as i64);

    for _ in 0..n {
        for (i, &el) in v.iter().enumerate() {
            s.add_lambda(s.apply(i as i64), el);
        }
    }
    let zero_in_w = s.apply(v.iter().position(|i| *i == 0).unwrap() as i64);

    v[s.reverse_apply((zero_in_w + 1000) % v.len() as i64) as usize]
        + v[s.reverse_apply((zero_in_w + 2000) % v.len() as i64) as usize]
        + v[s.reverse_apply((zero_in_w + 3000) % v.len() as i64) as usize]
}

fn main() {
    let mut v: Vec<i64> = common::get_problem_lines(2022, 20)
        .map(|x| x.parse::<i64>().unwrap())
        .collect();

    println!("part 1: {}", get_ans(&v, 1));

    v = v.into_iter().map(|v| v * 811589153).collect();

    println!("part 2: {}", get_ans(&v, 10));
}
