use std::collections::HashMap;

#[derive(Debug)]
struct Rock {
    width: isize,
    height: usize,
    shape: [i8; 4],
}

const ROCKS: [Rock; 5] = [
    Rock {
        width: 4,
        height: 1,
        shape: [0b0011110, 0b0000000, 0b0000000, 0b0000000],
    },
    Rock {
        width: 3,
        height: 3,
        shape: [0b0001000, 0b0011100, 0b0001000, 0b0000000],
    },
    Rock {
        width: 3,
        height: 3,
        shape: [0b0000100, 0b0000100, 0b0011100, 0b0000000],
    },
    Rock {
        width: 1,
        height: 4,
        shape: [0b0010000, 0b0010000, 0b0010000, 0b0010000],
    },
    Rock {
        width: 2,
        height: 2,
        shape: [0b0011000, 0b0011000, 0b0000000, 0b0000000],
    },
];

struct State {
    shaft: Vec<i8>,
    rock_index: usize,
    rock_top: usize,
    rock_offset: isize,
    shaft_height: usize,
    winds: Vec<bool>,
    wind_index: usize,
    time: usize,
}

//is this really not in the standard library?
fn off(a: i8, b: isize) -> i8 {
    if b < 0 {
        a << -b
    } else {
        a >> b
    }
}

impl State {
    fn add_rock(&mut self) {
        self.rock_index = (self.rock_index + 1) % 5;
        let rock = &ROCKS[self.rock_index];
        self.shaft.resize(self.shaft_height + 4 + rock.height, 0);
        self.rock_top = self.shaft.len() - 1;
        self.rock_offset = 0;
    }

    fn try_move(&mut self, delta_offset: isize, ndelta_depth: usize) -> bool {
        let offset = self.rock_offset + delta_offset;
        let new_top = self.rock_top - ndelta_depth;
        let rock = &ROCKS[self.rock_index];

        if offset < -2 || offset > 5 - rock.width {
            return false;
        }

        if (self.shaft[new_top] & off(rock.shape[0], offset) != 0)
            || (self.shaft[new_top - 1] & off(rock.shape[1], offset) != 0)
            || (self.shaft[new_top - 2] & off(rock.shape[2], offset) != 0)
            || (self.shaft[new_top - 3] & off(rock.shape[3], offset) != 0)
        {
            return false;
        }
        self.rock_offset = offset;
        self.rock_top = new_top;
        true
    }

    fn solidify(&mut self) {
        let rock = &ROCKS[self.rock_index];
        self.shaft_height = std::cmp::max(self.rock_top, self.shaft_height);
        self.shaft[self.rock_top] |= off(rock.shape[0], self.rock_offset);
        self.shaft[self.rock_top - 1] |= off(rock.shape[1], self.rock_offset);
        self.shaft[self.rock_top - 2] |= off(rock.shape[2], self.rock_offset);
        self.shaft[self.rock_top - 3] |= off(rock.shape[3], self.rock_offset);
    }

    fn init(s: &str) -> Self {
        State {
            rock_index: 4,
            rock_offset: 0,
            rock_top: 3,
            shaft: vec![0, 0, 0, 0b1111111],
            shaft_height: 3,
            winds: s.chars().map(|c| c == '<').collect(),
            wind_index: 0,
            time: 0,
        }
    }

    fn event_loop(&mut self, n: usize) {
        let mut solidified_rocks = 0;
        self.add_rock();
        loop {
            let is_left = self.winds[self.wind_index];
            self.wind_index = (self.wind_index + 1) % self.winds.len();
            self.time += 1;
            if is_left {
                self.try_move(-1, 0);
            } else {
                self.try_move(1, 0);
            }
            if !self.try_move(0, 1) {
                self.solidify();
                solidified_rocks += 1;
                if solidified_rocks == n {
                    return;
                }
                self.add_rock();
            }
        }
    }
}

impl std::fmt::Display for State {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        for (r, row) in self.shaft.iter().enumerate().rev() {
            for i in (0..7).rev() {
                if r <= self.rock_top && r > self.rock_top - 4 {
                    let rock = &ROCKS[self.rock_index];
                    if (off(rock.shape[self.rock_top - r], self.rock_offset) & (1 << i)) != 0 {
                        write!(f, "O")?;
                        continue;
                    }
                }
                if row & (1 << i) != 0 {
                    write!(f, "#")?;
                } else {
                    write!(f, ".")?;
                }
            }
            writeln!(f)?;
        }
        Ok(())
    }
}

fn big_event_loop(input: &str, bignum: usize) -> usize {
    let mut s = State::init(input);
    let mut snapshots: HashMap<(usize, Vec<i8>), (usize, usize)> = HashMap::new();
    let n = s.winds.len() * ROCKS.len(); //really lcm
    let mut num_rocks = 200;
    s.event_loop(200);
    loop {
        s.event_loop(1);
        num_rocks += 1;
        let new_snapshot: (usize, Vec<i8>) = (
            s.time % n,
            s.shaft.iter().skip(s.shaft.len() - 50).copied().collect(),
        );
        if let Some((old_num_rocks, old_height)) = snapshots.get(&new_snapshot) {
            let number_of_skips: usize = (bignum - old_num_rocks) / (num_rocks - old_num_rocks);
            let remaining =
                bignum - (old_num_rocks + number_of_skips * (num_rocks - old_num_rocks));
            let current_height = s.shaft_height;
            s.event_loop(remaining);
            return (s.shaft_height - current_height)
                + (current_height - old_height) * number_of_skips
                + old_height
                - 3;
        } else {
            snapshots.insert(new_snapshot, (num_rocks, s.shaft_height));
        }
    }
}

fn main() {
    let s: String = std::fs::read_to_string("inputs/17.txt").unwrap();
    let s = &s[0..s.len() - 1];

    let mut part1state = State::init(s);
    part1state.event_loop(2022);
    println!("part 1: {}", part1state.shaft_height - 3);

    println!("part 2: {}", big_event_loop(s, 1000000000000));
}
