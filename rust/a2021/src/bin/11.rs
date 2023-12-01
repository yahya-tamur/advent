fn ws(a: usize, b: usize) -> usize {
    usize::wrapping_add(usize::wrapping_add(a, !b), 1)
}

fn main() {
    let input = common::get_problem(2021, 11);
    let mut g: Vec<Vec<u8>> = input
        .lines()
        .map(|s| s.bytes().map(|x| x - b'0').collect())
        .collect();

    let (n, m) = (g.len(), g[0].len());

    let mut flashes = Vec::<(usize, usize)>::new();
    let mut total_flashes = 0;

    let mut k = 0;
    loop {
        if k == 100 {
            println!("part 1: {total_flashes}")
        }
        flashes.clear();
        for (i, row) in g.iter_mut().enumerate() {
            for (j, val) in row.iter_mut().enumerate() {
                *val += 1;
                if *val > 9 {
                    flashes.push((i, j));
                }
            }
        }
        let mut i = 0;
        while i < flashes.len() {
            let (r, c) = flashes[i];
            i += 1;
            for (r_, c_) in [
                (r + 1, ws(c, 1)),
                (r + 1, c),
                (r + 1, c + 1),
                (r, c + 1),
                (ws(r, 1), c + 1),
                (ws(r, 1), c),
                (ws(r, 1), ws(c, 1)),
                (r, ws(c, 1)),
            ] {
                if r_ >= n || c_ >= m {
                    continue;
                }
                g[r_][c_] += 1;
                if g[r_][c_] == 10 {
                    flashes.push((r_, c_));
                }
            }
        }

        total_flashes += flashes.len();
        for &(r, c) in flashes.iter() {
            g[r][c] = 0;
        }
        k += 1;
        if flashes.len() == n * m {
            println!("part 2: {k}");
            return;
        }
    }
}
