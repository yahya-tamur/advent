use std::collections::VecDeque;

fn ws

fn main() {
    let input = "5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
";
    let mut g: Vec<Vec<u8>> = input
        .lines()
        .map(|s| s.bytes().map(|x| x - b'0').collect())
        .collect();

    let (n, m) = (g.len(), g[0].len());

    let mut flashes = Vec::<(usize, usize)>::new();
    let mut total_flashes = 0;

    for _ in 0..10 {
        flashes.clear();
        for i in 0..n {
            for j in 0..m {
                g[i][j] += 1;
                if g[i][j] > 9 {
                    flashes.push((i, j));
                }
            }
        }
        let mut i = 0;
        while i < flashes.len() {
            let (r, c) = flashes[i];
            let (r, c) = 
            i += 1;
            for (r_, c_) in [
                (r + 1, c - 1),
                (r + 1, c),
                (r + 1, c + 1),
                (r, c + 1),
                (r - 1, c + 1),
                (r - 1, c),
                (r - 1, c - 1),
                (r, c - 1),
            ] {
                if r_ >= n || c_ >= m {
                    continue;
                }
                g[r_][c_] += 1;
                if g[r_][c_] == 9 {
                    flashes.push((r_, c_));
                }
            }
        }

        total_flashes += flashes.len();
        for &(r, c) in flashes.iter() {
            g[r][c] = 0;
        }
    }

    print!("{}", total_flashes);
}
