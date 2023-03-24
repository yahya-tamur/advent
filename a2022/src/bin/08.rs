use std::fs::File;
use std::io::{prelude::*, BufReader};

//v, n -> returns i so that v[i..] < n
fn binary_search(ix: &Vec<usize>, src: impl Fn(usize) -> u8, n: u8) -> usize {
    // [ , )
    let (mut left, mut right) = (0usize, ix.len());
    while left != right {
        // left <= mid < right
        let mid = (left + right) / 2;
        if src(ix[mid]) >= n {
            left = mid + 1; //always contracts
        } else {
            right = mid;
        }
    }
    left
}

type Transform = fn(usize, usize, usize) -> (usize, usize);

fn main() {
    let file = File::open("inputs/08.txt").unwrap();
    let input: Vec<Vec<u8>> = BufReader::new(file)
        .lines()
        .map(|x| x.unwrap().into_bytes())
        .collect();
    let n = input.len();

    //only works if forest is a square
    let transforms: [Transform; 4] = [
        |i, j, _n| (i, j),
        |i, j, n| (i, n - 1 - j),
        |i, j, _n| (j, i),
        |i, j, n| (n - 1 - j, i),
    ];

    let mut mask = vec![vec![false; n]; n];
    for t in transforms {
        for i in 0..n {
            let (fi, fj) = t(i, 0, n);
            let mut max = input[fi][fj];
            mask[fi][fj] = true;
            for j in 0..n {
                let (i, j) = t(i, j, n);
                if input[i][j] > max {
                    max = input[i][j];
                    mask[i][j] = true;
                }
            }
        }
    }

    println!(
        "{:?}",
        mask.iter()
            .map(|bs| bs.iter().map(|&b| b as i32).sum::<i32>())
            .sum::<i32>()
    );

    let mut vals = vec![vec![1usize; n]; n];
    for t in transforms {
        for i in 0..n {
            let mut vec = vec![]; //contains j-values, t(i,n) to t(i,n)
            for j in 0..n {
                let (ci, cj) = t(i, j, n);
                let k = binary_search(
                    &vec,
                    |p| {
                        let (r, s) = t(i, p, n);
                        input[r][s]
                    },
                    input[ci][cj],
                );
                vals[ci][cj] *= match k {
                    0 => j,
                    n => j - vec[n - 1],
                };
                vec.resize(k, 0);
                vec.push(j);
            }
        }
    }
    println!(
        "{:?}",
        vals.iter().map(|v| v.iter().max().unwrap()).max().unwrap()
    );
}
