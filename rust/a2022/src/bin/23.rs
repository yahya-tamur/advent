//felt very easy, especially after day 22.
//maybe there's a much faster way of doing this, but I kind of doubt it -- the array
//isn't much bigger than needed, and the constant factor should be small.
//
//similarly maybe this could be factored to be a little more concise but I didn't
//bother since the algorithm is very, very straightforward -- we just
//follow the instructions in the question.
//
//the only optimization is that we reuse the proposalpoint grid to avoid unnecessary
//heap allocations.

#[derive(Clone, PartialEq, Copy)]
enum Point {
    Emp,
    Elf,
}

struct PointRow<'a>(&'a Vec<Point>);

impl<'a> std::fmt::Display for PointRow<'a> {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> Result<(), std::fmt::Error> {
        for p in self.0.iter() {
            match p {
                Point::Emp => write!(f, ".")?,
                Point::Elf => write!(f, "#")?,
            }
        }
        Ok(())
    }
}

//elves can only move 10 blocks off the map in 10 iterations
//but just to make proposal calculating easier I added a couple
//extra
//
//so no need for arbitrary re-padding in part 1 but we do need to in part 2
const PAD: usize = 15;

fn parse(input: &str) -> Vec<Vec<Point>> {
    let lines: Vec<&str> = input.lines().collect();
    let (n, m) = (lines.len(), lines[0].len());

    let mut ans = vec![vec![Point::Emp; m + 2 * PAD]; n + 2 * PAD];

    for (r, &line) in lines.iter().enumerate() {
        for (c, ch) in line.chars().enumerate() {
            if ch == '#' {
                ans[r + PAD][c + PAD] = Point::Elf;
            }
        }
    }

    ans
}

#[derive(Debug, Clone)]
enum ProposalPoint {
    Empty,
    Proposed(usize, usize), //could be smaller
    Blocked,
}

fn iterate(input: &mut Vec<Vec<Point>>, pps: &mut [Vec<ProposalPoint>], start: usize) -> bool {
    let mut changed = false;
    for row in pps.iter_mut() {
        for el in row {
            *el = ProposalPoint::Empty;
        }
    }
    let mut update = |r: usize, c: usize, r_: usize, c_: usize| {
        pps[r_][c_] = match pps[r_][c_] {
            ProposalPoint::Empty => ProposalPoint::Proposed(r, c),
            ProposalPoint::Proposed(_, _) => ProposalPoint::Blocked,
            ProposalPoint::Blocked => ProposalPoint::Blocked,
        }
    };
    let dirs = ["north", "south", "west", "east"];
    for r in 1..(input.len() - 1) {
        for c in 1..(input[0].len() - 1) {
            for i in 0..4 {
                if input[r][c] != Point::Elf {
                    continue;
                }
                if input[r - 1][c - 1] == Point::Emp
                    && input[r - 1][c] == Point::Emp
                    && input[r - 1][c + 1] == Point::Emp
                    && input[r][c + 1] == Point::Emp
                    && input[r + 1][c + 1] == Point::Emp
                    && input[r + 1][c] == Point::Emp
                    && input[r + 1][c - 1] == Point::Emp
                    && input[r][c - 1] == Point::Emp
                {
                    continue;
                }
                match dirs[(start + i) % 4] {
                    "north" => {
                        if input[r - 1][c - 1] == Point::Emp
                            && input[r - 1][c] == Point::Emp
                            && input[r - 1][c + 1] == Point::Emp
                        {
                            changed = true;
                            update(r, c, r - 1, c);
                            break;
                        }
                    }
                    "south" => {
                        if input[r + 1][c - 1] == Point::Emp
                            && input[r + 1][c] == Point::Emp
                            && input[r + 1][c + 1] == Point::Emp
                        {
                            changed = true;
                            update(r, c, r + 1, c);
                            break;
                        }
                    }
                    "west" => {
                        if input[r - 1][c - 1] == Point::Emp
                            && input[r][c - 1] == Point::Emp
                            && input[r + 1][c - 1] == Point::Emp
                        {
                            changed = true;
                            update(r, c, r, c - 1);
                            break;
                        }
                    }
                    "east" => {
                        if input[r - 1][c + 1] == Point::Emp
                            && input[r][c + 1] == Point::Emp
                            && input[r + 1][c + 1] == Point::Emp
                        {
                            changed = true;
                            update(r, c, r, c + 1);
                            break;
                        }
                    }
                    _ => panic!("unrecognized direction"),
                }
            }
        }
    }

    for (r_, line) in pps.iter().enumerate() {
        for (c_, pp) in line.iter().enumerate() {
            if let &ProposalPoint::Proposed(r, c) = pp {
                input[r][c] = Point::Emp;
                input[r_][c_] = Point::Elf;
            }
        }
    }
    changed
}

fn get_starts(grid: &Vec<Vec<Point>>) -> (usize, usize, usize, usize) {
    let (n, m) = (grid.len(), grid[0].len());
    (
        (0..n)
            .find(|r| (0..m).any(|c| grid[*r][c] != Point::Emp))
            .unwrap(),
        (0..n)
            .rfind(|r| (0..m).any(|c| grid[*r][c] != Point::Emp))
            .unwrap(),
        (0..m)
            .find(|c| (0..n).any(|r| grid[r][*c] != Point::Emp))
            .unwrap(),
        (0..m)
            .rfind(|c| (0..n).any(|r| grid[r][*c] != Point::Emp))
            .unwrap(),
    )
}

fn part1(mut grid: Vec<Vec<Point>>) -> usize {
    let mut pps = vec![vec![ProposalPoint::Empty; grid[0].len()]; grid.len()];

    for i in 0..10 {
        iterate(&mut grid, &mut pps, i % 4);
        println!("after {} iterations:", i + 1);
        for line in grid.iter() {
            println!("{}", PointRow(line));
        }
    }

    let (a, b, c, d) = get_starts(&grid);

    let elf_count: usize = grid
        .iter()
        .map(|line| line.iter().filter(|x| **x == Point::Elf).count())
        .sum();

    (b - a + 1) * (d - c + 1) - elf_count
}

fn part2(mut grid: Vec<Vec<Point>>) -> usize {
    fn check_and_pad(g: &mut Vec<Vec<Point>>, pps: &mut Vec<Vec<ProposalPoint>>) {
        let (n, m) = (g.len(), g[0].len());
        let (a, b, c, d) = get_starts(g);
        if a <= 5 || n - b <= 5 || c <= 5 || m - d <= 5 {
            for row in g.iter_mut() {
                let mut newrow = vec![Point::Emp; 100];
                newrow.append(row);
                newrow.resize(newrow.len() + 100, Point::Emp);
                std::mem::swap(row, &mut newrow);
            }
            let mut newg = vec![vec![Point::Emp; g[0].len()]; 100];
            newg.append(g);
            newg.resize(newg.len() + 100, vec![Point::Emp; newg[0].len()]);
            std::mem::swap(&mut newg, g);
            pps.resize(g.len(), vec![ProposalPoint::Empty; g[0].len()]);
            for row in pps {
                row.resize(g[0].len(), ProposalPoint::Empty);
            }
        }
    }
    let mut i = 0;
    let mut pps = vec![vec![ProposalPoint::Empty; grid[0].len()]; grid.len()];
    while iterate(&mut grid, &mut pps, i % 4) {
        i += 1;
        check_and_pad(&mut grid, &mut pps);
    }
    println!("after {} iterations:", i + 1);
    for line in grid.iter() {
        println!("{}", PointRow(line));
    }

    i + 1
}

fn main() {
    let input = common::get_problem(2022, 23);
    println!("part 1: {}", part1(parse(&input)));
    println!("part 2: {}", part2(parse(&input)));
}
