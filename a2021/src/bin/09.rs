fn main() {
    let m = common::get_problem_lines(2021, 9)
        .map(|line| {
            line.into_bytes()
                .iter()
                .map(|b| b - b'0')
                .collect::<Vec<u8>>()
        })
        .collect::<Vec<Vec<u8>>>();
    let map = m
        .iter()
        .enumerate()
        .map(|(r, row)| {
            row.iter()
                .enumerate()
                .map(|(c, &x)| {
                    let up = r != 0 && x > m[r - 1][c];
                    let down = r != m.len() - 1 && x > m[r + 1][c];
                    let left = c != 0 && x > m[r][c - 1];
                    let right = c != row.len() - 1 && x > m[r][c + 1];
                    match () {
                        () if x == 9 => '█',
                        () if up && right && down && left => '╬',
                        () if up && right && down => '╠',
                        () if right && down && left => '╦',
                        () if down && left && up => '╣',
                        () if left && up && right => '╩',
                        () if up && right => '╚',
                        () if up && down => '║',
                        () if up && left => '╝',
                        () if right && down => '╔',
                        () if right && left => '═',
                        () if left && down => '╗',
                        () if up => '↑',
                        () if right => '→',
                        () if down => '↓',
                        () if left => '←',
                        () => 'O',
                    }
                })
                .collect::<Vec<char>>()
        })
        .collect::<Vec<Vec<char>>>();
    for line in map.iter() {
        for char in line.iter() {
            print!("{}", char);
        }
        println!();
    }
    // shows that there are no ambiguous cases for which basin a low point goes to.

    let mut lp: Vec<(usize, usize)> = Vec::new();
    for (r, row) in m.iter().enumerate() {
        for (c, &x) in row.iter().enumerate() {
            if (r == 0 || x < m[r - 1][c])
                && (r == m.len() - 1 || x < m[r + 1][c])
                && (c == 0 || x < m[r][c - 1])
                && (c == row.len() - 1 || x < m[r][c + 1])
            {
                lp.push((r, c));
            }
        }
    }
    println!("part 1: {}", lp.len());

    let mut visited: Vec<Vec<bool>> = vec![vec![false; m[0].len()]; m.len()];
    let mut basin_sizes = lp
        .iter()
        .map(|&p| {
            let mut active_nodes: Vec<(usize, usize)> = vec![p];
            let mut basin = 0;
            while let Some((r, c)) = active_nodes.pop() {
                if m[r][c] == 9 || visited[r][c] {
                    continue;
                }
                basin += 1;
                visited[r][c] = true;

                if r != 0 {
                    active_nodes.push((r - 1, c));
                }
                if r != m.len() - 1 {
                    active_nodes.push((r + 1, c));
                }
                if c != 0 {
                    active_nodes.push((r, c - 1));
                }
                if c != m[0].len() - 1 {
                    active_nodes.push((r, c + 1));
                }
            }
            basin
        })
        .collect::<Vec<usize>>();
    basin_sizes.sort();
    let l = basin_sizes.len() - 1;

    println!(
        "part 2: {}",
        basin_sizes[l] * basin_sizes[l - 1] * basin_sizes[l - 2]
    );
}
