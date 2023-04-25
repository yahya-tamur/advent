///0b1 = up, 0b01 = right, 0b100 = down, 0b1000 = left

#[allow(dead_code)]
fn print_state(grid: &[Vec<u8>], state: &[Vec<bool>]) {
    for (r, line) in grid.iter().enumerate() {
        for (c, point) in line.iter().enumerate() {
            print!(
                "{}",
                match point {
                    0b1 => "^",
                    0b10 => ">",
                    0b100 => "v",
                    0b1000 => "<",
                    0b0011 | 0b0101 | 0b1001 | 0b0110 | 0b1010 | 0b1100 => "2",
                    0b0111 | 0b1011 | 0b1101 | 0b1110 => "3",
                    0b1111 => "4",
                    0 =>
                        if state[r][c] {
                            "@"
                        } else {
                            " "
                        },
                    _ => "?",
                }
            );
        }
        println!();
    }
}

fn parse(input: &str) -> Vec<Vec<u8>> {
    let mut it = input.lines();
    it.next();
    it.take_while(|s| s.as_bytes()[1] != b'#')
        .map(|s| {
            let mut it = s.chars();
            it.next();
            it.take_while(|c| *c != '#')
                .map(|c| match c {
                    '^' => 0b1,
                    '>' => 0b10,
                    'v' => 0b100,
                    '<' => 0b1000,
                    '.' | '#' => 0,
                    a => panic!("unknown char {a}"),
                })
                .collect()
        })
        .collect()
}

fn wrap(k: isize, n: isize) -> usize {
    k.rem_euclid(n) as usize
}

fn advance(grid: &mut Vec<Vec<u8>>, swap: &mut Vec<Vec<u8>>) {
    let (n, m) = (grid.len() as isize, grid[0].len() as isize);
    for r in 0..n {
        for c in 0..m {
            swap[r as usize][c as usize] = (grid[wrap(r + 1, n)][c as usize] & 0b1)
                | (grid[wrap(r - 1, n)][c as usize] & 0b100)
                | (grid[r as usize][wrap(c + 1, m)] & 0b1000)
                | (grid[r as usize][wrap(c - 1, m)] & 0b10);
        }
    }
    std::mem::swap(grid, swap);
}

fn iterate(grid: &mut Vec<Vec<u8>>, goals: Vec<(usize, usize)>) {
    let (n, m) = (grid.len(), grid[0].len());
    let mut swapgrid = vec![vec![0; m]; n];

    let mut state = vec![vec![false; m]; n];
    let mut swapstate = vec![vec![false; m]; n];

    let (n, m) = (n as isize, m as isize);

    let mut iterations = 0;
    let mut goals_iter = goals.iter();
    let (mut start_r, mut start_c) = goals_iter.next().unwrap();

    let mut first_goal_met = false;
    for (goal_r, goal_c) in goals_iter {
        for line in state.iter_mut() {
            for x in line.iter_mut() {
                *x = false;
            }
        }
        loop {
            advance(grid, &mut swapgrid);
            for r in 0..n {
                for c in 0..m {
                    swapstate[r as usize][c as usize] = grid[r as usize][c as usize] == 0
                        && (state[r as usize][c as usize]
                            || r >= 1 && state[r as usize - 1][c as usize]
                            || r < n - 1 && state[r as usize + 1][c as usize]
                            || c >= 1 && state[r as usize][c as usize - 1]
                            || c < m - 1 && state[r as usize][c as usize + 1]);
                }
            }
            swapstate[start_r][start_c] = grid[start_r][start_c] == 0;
            std::mem::swap(&mut state, &mut swapstate);
            iterations += 1;
            if state[*goal_r][*goal_c] {
                break;
            }
            //print_state(&grid, &state);
            //println!("")
        }
        advance(grid, &mut swapgrid);
        iterations += 1;
        (start_r, start_c) = (*goal_r, *goal_c);
        if !first_goal_met {
            println!("part 1: {}", iterations);
            first_goal_met = true;
        }
    }
    println!("part 2: {}", iterations);
}

fn main() {
    let file = common::get_problem(2022, 24);
    let mut v = parse(&file);
    let (n, m) = (v.len(), v[0].len());
    //iterate is what prints out the answer for efficiency reasons --
    //it's better to call it once with a longer sequence of instructions
    //instead of several times with shorter sequences since it heap allocates
    //buffers on every call.
    iterate(&mut v, vec![(0, 0), (n - 1, m - 1), (0, 0), (n - 1, m - 1)]);
}
