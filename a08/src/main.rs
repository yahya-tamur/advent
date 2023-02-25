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

fn main() {
    let file = File::open("input.txt").unwrap();
    let input: Vec<Vec<u8>> = BufReader::new(file)
        .lines()
        .map(|x| x.unwrap().into_bytes())
        .collect();
    let n = input.len();

    //only works if forest is a square
    let transforms: [Box<dyn Fn(usize, usize) -> (usize, usize)>; 4] = [
        Box::new(|i, j| (i, j)),
        Box::new(|i, j| (i, n - 1 - j)),
        Box::new(|i, j| (j, i)),
        Box::new(|i, j| (n - 1 - j, i)),
    ];

    let mut mask = vec![vec![false; n]; n];
    for t in &transforms {
        for i in 0..n {
            let (fi, fj) = t(i, 0);
            let mut max = input[fi][fj];
            mask[fi][fj] = true;
            for j in 0..n {
                let (i, j) = t(i, j);
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
    for t in &transforms {
        for i in 0..n {
            let mut vec = vec![]; //contains j-values, t(i,n) to t(i,n)
            for j in 0..n {
                let (ci, cj) = t(i, j);
                let k = binary_search(
                    &vec,
                    |p| {
                        let (r, s) = t(i, p);
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
