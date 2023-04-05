// This took me a lot of time.
// I deleted the tests after it started getting the right answer

use regex::Regex;

#[derive(Debug)]
enum Instruction {
    Forward(i32),
    Left,
    Right,
}

#[derive(Clone, Debug, PartialEq, Eq, Copy)]
enum Point {
    Valid,
    Wall,
    Empty,
}

type Map = Vec<Vec<Point>>;

#[derive(Debug, Clone, Copy)]
pub enum Dir {
    Right,
    Down,
    Left,
    Up,
}

pub fn add(a: Dir, b: Dir) -> Dir {
    from_int((to_int(a) + to_int(b)) % 4)
}

pub fn op(a: Dir) -> Dir {
    from_int((4 - to_int(a)) % 4)
}

pub fn to_int(d: Dir) -> u8 {
    match d {
        Dir::Right => 0,
        Dir::Down => 1,
        Dir::Left => 2,
        Dir::Up => 3,
    }
}

fn from_int(i: u8) -> Dir {
    match i {
        0 => Dir::Right,
        1 => Dir::Down,
        2 => Dir::Left,
        3 => Dir::Up,
        _ => panic!("invalid direction"),
    }
}

fn parse(f: &str) -> (Map, Vec<Instruction>) {
    let mut s: Vec<&str> = f.lines().collect();

    let final_line = s.pop().unwrap();

    s.pop();

    let n = s.len();
    let m = s.iter().map(|v| v.len()).max().unwrap();

    let mut grid: Map = vec![vec![Point::Empty; m]; n];
    for (r, &ss) in s.iter().enumerate() {
        for (c, ch) in ss.chars().enumerate() {
            match ch {
                '.' => grid[r][c] = Point::Valid,
                '#' => grid[r][c] = Point::Wall,
                ' ' => {}
                _ => panic!("error parsing grid"),
            }
        }
    }

    let instr_regex = Regex::new(r"(?P<num>\d+)|(?P<l>L)|(?P<r>R)").unwrap();

    (
        grid,
        instr_regex
            .captures_iter(final_line)
            .map(|cap| match () {
                () if cap.name("num").is_some() => {
                    Instruction::Forward(cap.name("num").unwrap().as_str().parse().unwrap())
                }
                () if cap.name("l").is_some() => Instruction::Left,
                () if cap.name("r").is_some() => Instruction::Right,
                _ => panic!("error parsing instructions"),
            })
            .collect(),
    )
}

trait CoordinateManager {
    fn initialize(v: &Map) -> Self;

    //notice that right is 0, so to turn 90*, we turn up or down. for 180*, left.
    fn turn(&mut self, dir: Dir);

    fn step(&mut self);

    fn get_location(&self) -> (usize, usize, Dir);

    fn follow(grid: &Map, instrs: &Vec<Instruction>) -> usize
    where
        Self: Sized,
    {
        let mut cm = Self::initialize(grid);
        for instr in instrs {
            match instr {
                Instruction::Left => cm.turn(Dir::Up),
                Instruction::Right => cm.turn(Dir::Down),
                Instruction::Forward(n) => {
                    for _ in 0..*n {
                        cm.step();
                        let (nr, nc, _) = cm.get_location();
                        if grid[nr][nc] == Point::Wall {
                            cm.turn(Dir::Left);
                            cm.step();
                            cm.turn(Dir::Left);
                            break;
                        }
                    }
                }
            }
        }
        let (r, c, d) = cm.get_location();
        1000 * (r + 1) + 4 * (c + 1) + to_int(d) as usize
    }
}

mod ncm {
    use crate::{add, CoordinateManager, Dir, Map, Point};

    pub struct NaiveCoordinateManager {
        r: usize,
        c: usize,
        dir: Dir,
        h_bounds: Vec<(usize, usize)>,
        v_bounds: Vec<(usize, usize)>,
    }

    impl CoordinateManager for NaiveCoordinateManager {
        fn initialize(grid: &Map) -> Self {
            let (n, m) = (grid.len(), grid[0].len());
            NaiveCoordinateManager {
                r: 0,
                c: grid[0].iter().position(|c| *c != Point::Empty).unwrap(),
                dir: Dir::Right,
                h_bounds: grid
                    .iter()
                    .map(|r| {
                        (
                            r.iter().position(|c| *c != Point::Empty).unwrap(),
                            r.iter().rposition(|c| *c != Point::Empty).unwrap(),
                        )
                    })
                    .collect(),
                v_bounds: (0..m)
                    .map(|j| {
                        (
                            (0..n).find(|&i| grid[i][j] != Point::Empty).unwrap(),
                            (0..n).rfind(|&i| grid[i][j] != Point::Empty).unwrap(),
                        )
                    })
                    .collect(),
            }
        }

        fn turn(&mut self, dir: Dir) {
            self.dir = add(self.dir, dir);
        }

        fn step(&mut self) {
            match self.dir {
                Dir::Right => {
                    self.c = if self.c == self.h_bounds[self.r].1 {
                        self.h_bounds[self.r].0
                    } else {
                        self.c + 1
                    }
                }
                Dir::Down => {
                    self.r = if self.r == self.v_bounds[self.c].1 {
                        self.v_bounds[self.c].0
                    } else {
                        self.r + 1
                    };
                }
                Dir::Left => {
                    self.c = if self.c == self.h_bounds[self.r].0 {
                        self.h_bounds[self.r].1
                    } else {
                        self.c - 1
                    };
                }
                Dir::Up => {
                    self.r = if self.r == self.v_bounds[self.c].0 {
                        self.v_bounds[self.c].1
                    } else {
                        self.r - 1
                    };
                }
            };
        }

        fn get_location(&self) -> (usize, usize, Dir) {
            (self.r, self.c, self.dir)
        }
    }
}

mod cube {
    use crate::{add, op, to_int, CoordinateManager, Dir, Map, Point};
    use std::collections::HashMap;

    #[derive(PartialEq, Eq, Hash, Clone, Copy, Debug)]
    enum Face {
        Top,
        Bottom,
        Left,
        Right,
        Front,
        Back,
    }

    const fn edge(f: Face, d: Dir) -> (Face, Dir) {
        match (f, d) {
            (Face::Front, Dir::Up) => (Face::Top, Dir::Up),
            (Face::Front, Dir::Right) => (Face::Right, Dir::Right),
            (Face::Front, Dir::Down) => (Face::Bottom, Dir::Down),
            (Face::Front, Dir::Left) => (Face::Left, Dir::Left),
            (Face::Top, Dir::Up) => (Face::Back, Dir::Up),
            (Face::Top, Dir::Right) => (Face::Right, Dir::Down),
            (Face::Top, Dir::Down) => (Face::Front, Dir::Down),
            (Face::Top, Dir::Left) => (Face::Left, Dir::Down),
            (Face::Right, Dir::Up) => (Face::Top, Dir::Left),
            (Face::Right, Dir::Right) => (Face::Back, Dir::Left),
            (Face::Right, Dir::Down) => (Face::Bottom, Dir::Left),
            (Face::Right, Dir::Left) => (Face::Front, Dir::Left),
            (Face::Left, Dir::Up) => (Face::Top, Dir::Right),
            (Face::Left, Dir::Right) => (Face::Front, Dir::Right),
            (Face::Left, Dir::Down) => (Face::Bottom, Dir::Right),
            (Face::Left, Dir::Left) => (Face::Back, Dir::Right),
            (Face::Bottom, Dir::Up) => (Face::Front, Dir::Up),
            (Face::Bottom, Dir::Right) => (Face::Right, Dir::Up),
            (Face::Bottom, Dir::Down) => (Face::Back, Dir::Down),
            (Face::Bottom, Dir::Left) => (Face::Left, Dir::Up),
            (Face::Back, Dir::Up) => (Face::Bottom, Dir::Up),
            (Face::Back, Dir::Right) => (Face::Right, Dir::Left),
            (Face::Back, Dir::Down) => (Face::Top, Dir::Down),
            (Face::Back, Dir::Left) => (Face::Left, Dir::Right),
        }
    }

    #[derive(Debug)]
    struct FaceChart {
        topleft: (usize, usize),
        dir: Dir,
    }

    #[derive(Debug)]
    pub struct CubeCoordinateManager {
        fm: HashMap<Face, FaceChart>,
        face: Face,
        row: usize,
        col: usize,
        dir: Dir,
        n: usize,
    }

    impl CoordinateManager for CubeCoordinateManager {
        fn turn(&mut self, dir: Dir) {
            self.dir = add(self.dir, dir);
        }

        fn initialize(map: &Map) -> Self {
            let total: usize = map
                .iter()
                .map(|v| v.iter().filter(|x| **x != Point::Empty).count())
                .sum();

            let n = ((total / 6) as f64).sqrt() as isize;
            let mut fm: HashMap<Face, FaceChart> = HashMap::new();

            struct VisitContext<'a> {
                map: &'a Map,
                n: isize,
                fm: &'a mut HashMap<Face, FaceChart>,
            }

            fn visit(vc: &mut VisitContext, r: isize, c: isize, turns: Dir, face: Face) {
                vc.fm.insert(
                    face,
                    FaceChart {
                        topleft: (r as usize, c as usize),
                        dir: turns, // 4 - turns?
                    },
                );
                let to_check = [
                    (0, -vc.n, Dir::Left),
                    (0, vc.n, Dir::Right),
                    (-vc.n, 0, Dir::Up),
                    (vc.n, 0, Dir::Down),
                ];

                for (dr, dc, dd) in to_check.iter() {
                    let (r_, c_) = (r + dr, c + dc);
                    if r_ >= 0
                        && c_ >= 0
                        && (r_ as usize) < vc.map.len()
                        && (c_ as usize) < vc.map[0].len()
                        && vc.map[r_ as usize][c_ as usize] != Point::Empty
                    {
                        let (face_, turns_) = edge(face, add(*dd, turns));
                        if vc.fm.get(&face_).is_none() {
                            visit(vc, r + dr, c + dc, add(turns_, op(*dd)), face_);
                        }
                    }
                }
            }
            visit(
                &mut VisitContext {
                    map,
                    n,
                    fm: &mut fm,
                },
                0,
                map[0].iter().position(|x| *x != Point::Empty).unwrap() as isize,
                Dir::Right,
                Face::Front,
            );
            CubeCoordinateManager {
                fm,
                face: Face::Front,
                row: 0,
                col: 0,
                dir: Dir::Right,
                n: n as usize - 1, //0..n inclusive are valid. so n-k is valid for valid k
            }
        }

        fn get_location(&self) -> (usize, usize, Dir) {
            let fc = self.fm.get(&self.face).unwrap();
            let (mut r, mut c) = (self.row, self.col);

            for _ in 0..to_int(op(fc.dir)) {
                (r, c) = (c, self.n - r);
            }

            (
                fc.topleft.0 + r,
                fc.topleft.1 + c,
                add(self.dir, op(fc.dir)),
            )
        }

        fn step(&mut self) {
            //offset is offset from you to the corner on *your* left (facing dir)
            fn changedir(s: &mut CubeCoordinateManager, offset: usize) {
                match s.dir {
                    Dir::Right => {
                        s.row = offset;
                        s.col = 0;
                    }
                    Dir::Left => {
                        s.row = s.n - offset;
                        s.col = s.n;
                    }
                    Dir::Up => {
                        s.row = s.n;
                        s.col = offset;
                    }
                    Dir::Down => {
                        s.row = 0;
                        s.col = s.n - offset;
                    }
                }
            }
            match self.dir {
                dd @ Dir::Right => {
                    if self.col == self.n {
                        (self.face, self.dir) = edge(self.face, dd);
                        changedir(self, self.row);
                    } else {
                        self.col += 1;
                    }
                }
                dd @ Dir::Left => {
                    if self.col == 0 {
                        (self.face, self.dir) = edge(self.face, dd);
                        changedir(self, self.n - self.row);
                    } else {
                        self.col -= 1;
                    }
                }
                dd @ Dir::Down => {
                    if self.row == self.n {
                        (self.face, self.dir) = edge(self.face, dd);
                        changedir(self, self.n - self.col);
                    } else {
                        self.row += 1;
                    }
                }
                dd @ Dir::Up => {
                    if self.row == 0 {
                        (self.face, self.dir) = edge(self.face, dd);
                        changedir(self, self.col);
                    } else {
                        self.row -= 1;
                    }
                }
            }
        }
    }
}

fn main() {
    let f = std::fs::read_to_string("inputs/22.txt").unwrap();
    let (grid, instructions) = parse(&f);

    println!(
        "part1: {:#?}",
        ncm::NaiveCoordinateManager::follow(&grid, &instructions)
    );

    println!(
        "part2: {:#?}",
        cube::CubeCoordinateManager::follow(&grid, &instructions)
    );
}
