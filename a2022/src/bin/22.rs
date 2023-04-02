use regex::Regex;

#[derive(Debug)]
enum Instruction {
    Forward(i32),
    Left,
    Right,
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum Point {
    Valid,
    Wall,
    Empty,
}

type Map = Vec<Vec<Point>>;
type Dir = u8;

fn parse(f: &str) -> (Map, Vec<Instruction>) {
    let mut s: Vec<&str> = f.lines().collect();

    let final_line = s.pop().unwrap();

    let instr_regex = Regex::new(r"(?P<num>\d+)|(?P<l>L)|(?P<r>R)").unwrap();

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
                _ => panic!(""),
            }
        }
    }
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
                _ => panic!("AAAA!!!AAA!!!AAAA!!!"),
            })
            .collect(),
    )
}

trait CoordinateManager {
    //not great that we need the Map for initialize then again for follow
    //but initialize only looks at the general shape, follow uses the nodes
    fn initialize(v: &Map) -> Self;

    fn step(&mut self, dir: Dir);

    fn get_coordinates(&self) -> (usize, usize);

    fn follow(&mut self, grid: &Map, instrs: &Vec<Instruction>) -> usize {
        let mut dir = 0; // right to up, 0 to 3, clockwise
        for instr in instrs {
            match instr {
                Instruction::Left => {
                    dir = (dir + 3) % 4;
                }
                Instruction::Right => {
                    dir = (dir + 1) % 4;
                }
                Instruction::Forward(n) => {
                    for _ in 0..*n {
                        self.step(dir);
                        let (nr, nc) = self.get_coordinates();
                        if grid[nr][nc] == Point::Wall {
                            self.step((dir + 2) % 4);
                            break;
                        }
                    }
                }
            }
        }
        let (r, c) = self.get_coordinates();
        1000 * (r + 1) + 4 * (c + 1) + dir as usize
    }
}

mod ncm {
    use crate::{CoordinateManager, Dir, Map, Point};

    pub struct NaiveCoordinateManager {
        r: usize,
        c: usize,
        h_bounds: Vec<(usize, usize)>,
        v_bounds: Vec<(usize, usize)>,
    }

    impl CoordinateManager for NaiveCoordinateManager {
        fn initialize(grid: &Map) -> Self {
            let n = grid.len();
            let m = grid.iter().map(|ss| ss.len()).max().unwrap();
            NaiveCoordinateManager {
                r: 0,
                c: grid[0].iter().position(|c| *c != Point::Empty).unwrap(),
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
        fn step(&mut self, dir: Dir) {
            match dir {
                0 => {
                    self.c = if self.c == self.h_bounds[self.r].1 {
                        self.h_bounds[self.r].0
                    } else {
                        self.c + 1
                    }
                }
                1 => {
                    self.r = if self.r == self.v_bounds[self.c].1 {
                        self.v_bounds[self.c].0
                    } else {
                        self.r + 1
                    };
                }
                2 => {
                    self.c = if self.c == self.h_bounds[self.r].0 {
                        self.h_bounds[self.r].1
                    } else {
                        self.c - 1
                    };
                }
                3 => {
                    self.r = if self.r == self.v_bounds[self.c].0 {
                        self.v_bounds[self.c].1
                    } else {
                        self.r - 1
                    };
                }
                _ => panic!(""),
            };
        }

        fn get_coordinates(&self) -> (usize, usize) {
            (self.r, self.c)
        }
    }
}

mod cube {
    use crate::{CoordinateManager, Dir, Map, Point};

    #[derive(Debug, PartialEq, Eq, Clone)]
    struct Face {
        topleft: (usize, usize),
        dir: Dir,
    }

    impl Default for Face {
        fn default() -> Self {
            Face {
                //didn't want to make these Option's but
                //they do get set one by one during initialization.
                topleft: (99999, 99999),
                dir: 0,
            }
        }
    }

    #[derive(Default, Debug, PartialEq, Eq, Clone)]
    pub struct Cube {
        n: usize,
        row: usize,
        column: usize,
        front: Face,
        back: Face,
        up: Face,
        right: Face,
        down: Face,
        left: Face,
    }

    //there's no way to see future step:
    //program will move, see if it's a wall and in that case, move in the opposite
    //direction.
    //
    //cube always looks like
    //  D
    //E A F
    //  B
    //  C
    //
    //gets refolded

    impl Cube {
        fn clockwise(&mut self) {
            std::mem::swap(&mut self.up, &mut self.right);
            std::mem::swap(&mut self.left, &mut self.up);
            std::mem::swap(&mut self.down, &mut self.left);

            self.front.dir = (self.front.dir + 1) % 4;
            self.up.dir = (self.up.dir + 1) % 4;
            self.right.dir = (self.right.dir + 1) % 4;
            self.down.dir = (self.down.dir + 1) % 4;
            self.left.dir = (self.left.dir + 1) % 4;
            self.back.dir = (self.back.dir + 3) % 4;
        }

        fn turn_to_up(&mut self) {
            std::mem::swap(&mut self.up, &mut self.front);
            std::mem::swap(&mut self.back, &mut self.up);
            std::mem::swap(&mut self.down, &mut self.back);
            self.left.dir = (self.left.dir + 1) % 4;
            self.right.dir = (self.right.dir + 3) % 4;
        }

        // :(
        fn turn_to(&mut self, dir: Dir) {
            //a becomes b, b becomes c, c becomes d, d becomes a
            fn swap4(a: &mut Face, b: &mut Face, c: &mut Face, d: &mut Face) {
                std::mem::swap(a, b);
                std::mem::swap(b, c);
                std::mem::swap(c, d);
            }

            fn cw(a: &mut Face) {
                a.dir = (a.dir + 3) % 4;
            }

            fn ccw(a: &mut Face) {
                a.dir = (a.dir + 1) % 4;
            }

            match dir {
                1 => {
                    swap4(
                        &mut self.front,
                        &mut self.down,
                        &mut self.back,
                        &mut self.up,
                    );
                    ccw(&mut self.left);
                    cw(&mut self.right);
                }
                3 => {
                    swap4(
                        &mut self.front,
                        &mut self.up,
                        &mut self.back,
                        &mut self.down,
                    );
                    cw(&mut self.left);
                    ccw(&mut self.right);
                }
                2 => {
                    swap4(
                        &mut self.front,
                        &mut self.left,
                        &mut self.back,
                        &mut self.right,
                    );
                    cw(&mut self.up);
                    ccw(&mut self.down);
                }
                0 => {
                    swap4(
                        &mut self.front,
                        &mut self.right,
                        &mut self.back,
                        &mut self.left,
                    );
                    ccw(&mut self.up);
                    cw(&mut self.down);
                }
                _ => panic!(),
            }
        }
    }
    impl CoordinateManager for Cube {
        fn step(&mut self, dir: Dir) {
            match dir {
                0 => {
                    if self.column == self.n - 1 {
                        self.turn_to(0);
                        self.column = 0;
                    } else {
                        self.column += 1;
                    }
                }
                1 => {
                    if self.row == self.n - 1 {
                        self.turn_to(1);
                        self.row = 0;
                    } else {
                        self.row += 1;
                    }
                }
                2 => {
                    if self.column == 0 {
                        self.turn_to(2);
                        self.column = self.n - 1;
                    } else {
                        self.column -= 1;
                    }
                }
                3 => {
                    if self.row == 0 {
                        self.turn_to(3);
                        self.row = self.n - 1;
                    } else {
                        self.row -= 1;
                    }
                }
                _ => panic!(""),
            }
        }

        fn get_coordinates(&self) -> (usize, usize) {
            println!("local: {} {}", self.row, self.column);
            println!("topleft: {:?}", self.front.topleft);
            println!("topdir: {}", self.front.dir);
            println!();
            let mut r = self.row;
            let mut c = self.column;
            for _ in 0..self.front.dir {
                let temp = r;
                r = c;
                c = self.n - 1 - temp;
            }
            /*
            while self.front.dir != 0 {
                self.clockwise();
            }
            */
            let (row, column) = self.front.topleft;
            (row + r, column + c)
        }

        fn initialize(grid: &Map) -> Self {
            let total: usize = grid
                .iter()
                .map(|v| v.iter().filter(|c| **c != Point::Empty).count())
                .sum();

            let mut cube = Cube::default();
            cube.n = ((total / 6) as f64).sqrt() as usize;

            let start = grid[0].iter().position(|c| *c != Point::Empty).unwrap();

            fn visit(grid: &Map, cube: &mut Cube, r: isize, c: isize, depth: usize) {
                //println!("depth {} got: {:#?}", depth, cube);
                cube.front.topleft = (r as usize, c as usize);
                cube.front.dir = 0;
                let n = cube.n as isize;
                let check = |r: isize, c: isize| {
                    r >= 0
                        && c >= 0
                        && r < grid.len() as isize
                        && c < grid[0].len() as isize
                        && grid[r as usize][c as usize] != Point::Empty
                };

                if check(r - n, c) {
                    cube.turn_to(3);
                    //println!("depth {} turning up", depth);
                    if cube.front.topleft.0 == 99999 {
                        //println!("   visiting");
                        visit(grid, cube, r - n, c, depth + 1);
                    }
                    cube.turn_to(1);
                }
                if check(r + n, c) {
                    cube.turn_to(1);
                    //println!("depth {} turning down", depth);
                    if cube.front.topleft.0 == 99999 {
                        //println!("   visiting");
                        visit(grid, cube, r + n, c, depth + 1);
                    }
                    cube.turn_to(3);
                }
                if check(r, c - n) {
                    cube.turn_to(2);
                    //println!("depth {} turning left", depth);
                    if cube.front.topleft.0 == 99999 {
                        //println!("   visiting");
                        visit(grid, cube, r, c - n, depth + 1);
                    }
                    cube.turn_to(0);
                }
                if check(r, c + n) {
                    cube.turn_to(0);
                    //println!("depth {} turning right", depth);
                    if cube.front.topleft.0 == 99999 {
                        //println!("   visiting");
                        visit(grid, cube, r, c + n, depth + 1);
                    }
                    cube.turn_to(2);
                }
            }

            visit(grid, &mut cube, 0, start as isize, 0);

            cube
        }
    }

    #[test]
    fn turnonce() {
        const CUBE: &str = "  ....\n  ....\n  ..\n  ..\n....\n....\n..\n..\n\n5";

        let (testgrid, _) = crate::parse(&CUBE);
        let mut test = Cube::initialize(&testgrid);
        println!("final cube: {:#?}", test);
        //  println!("INITIAL: {:#?}", test);
        //  test.turn_to(3);
        //  println!("AFTER TURN UP: {:#?}", test);
        panic!();
    }
}

#[cfg(test)]
mod cubetest {
    use crate::*;

    const CUBE: &str = "  ....\n  ....\n  ..\n  ..\n....\n....\n..\n..\n\n5";
    const RIGHT: [(usize, usize); 8] = [
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (5, 3),
        (5, 2),
        (5, 1),
        (5, 0),
    ];
    const DOWN: [(usize, usize); 8] = [
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 2),
        (4, 2),
        (5, 2),
        (6, 1),
        (6, 0),
    ];

    #[test]
    fn walk() {
        let (testgrid, _) = parse(&CUBE);
        let mut test = cube::Cube::initialize(&testgrid);
        println!("{:#?}", test);
        for i in 1..=8 {
            println!("{}", i);
            test.step(0);
            assert_eq!(test.get_coordinates(), RIGHT[i % 8]);
        }
        for i in 1..=8 {
            test.step(1);
            assert_eq!(test.get_coordinates(), DOWN[i % 8]);
        }
        for i in 1..=8 {
            test.step(2);
            assert_eq!(test.get_coordinates(), RIGHT[(8 - i) % 8]);
        }
        for i in 1..=8 {
            test.step(3);
            println!("{:#?}", test);
            assert_eq!(test.get_coordinates(), DOWN[(8 - i) % 8]);
        }
    }
}

fn main() {
    let f = std::fs::read_to_string("inputs/22.txt").unwrap();
    let (grid, instructions) = parse(&f);

    let mut part1 = ncm::NaiveCoordinateManager::initialize(&grid);

    println!("part1: {:#?}", part1.follow(&grid, &instructions));

    /*let (testgrid, _) = parse(&test);
        let mut test = cube::Cube::initialize(&testgrid);
        test.step(2);
        println!("{:?}", test.get_coordinates());
        test.step(2);
        println!("{:?}", test.get_coordinates());
        test.step(2);
        println!("{:?}", test.get_coordinates());
        test.step(2);
        println!("{:?}", test.get_coordinates());
        test.step(2);
        println!("{:?}", test.get_coordinates());
        test.step(2);
        println!("{:?}", test.get_coordinates());
        test.step(2);
        println!("{:?}", test.get_coordinates());
        test.step(2);
        println!("{:?}", test.get_coordinates());
        test.step(2);
        println!("{:?}", test.get_coordinates());
        test.step(2);
        println!("{:?}", test.get_coordinates());
    */
    //let mut part2 = cube::Cube::initialize(&grid);

    //println!("part2: {:#?}", part2.follow(&grid, &instructions));
}
