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

#[derive(Debug)]
struct State {
    shaft: Vec<i8>,
    rock_index: usize,
    rock_top: usize,
    rock_offset: isize,
    shaft_height: usize,
}

fn off(a: i8, b: isize) -> i8 {
    if b < 0 {
        a << -b
    } else {
        a >> b
    }
}

impl State {
    fn add_rock(&mut self) {
        self.rock_index += 1;
        if self.rock_index == 5 {
            self.rock_index = 0;
        }
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

    fn init() -> Self {
        State {
            rock_index: 4,
            rock_offset: 0,
            rock_top: 3,
            shaft: vec![0, 0, 0, 0b1111111],
            shaft_height: 3,
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
            write!(f, "\n")?;
        }
        Ok(())
    }
}

fn event_loop(state: &mut State, events: impl Iterator<Item = bool>, n: usize) {
    let mut solidified_rocks = 0;
    state.add_rock();
    for is_left in events {
        if is_left {
            state.try_move(-1, 0);
        } else {
            state.try_move(1, 0);
        }
        if !state.try_move(0, 1) {
            state.solidify();
            solidified_rocks += 1;
            if solidified_rocks == n {
                return;
            }
            state.add_rock();
        }
    }
}

fn big_event_loop(events: impl Iterator<Item = bool>, mod_events: usize, bignum: usize) {
    let mut s = State::init();
    event_loop(&mut s, events, mod_events);
    let tip: Vec<i8> = s
        .shaft
        .iter()
        .skip(s.shaft.len() - 500)
        .map(|x| *x)
        .collect();
    let prev_height = 
}

fn main() {
    let s: String = std::fs::read_to_string("inputs/17.txt").unwrap();
    let s = &s[0..s.len() - 1];
    println!("{:?}", s.len());
    let mut state = State {
        rock_index: 4,
        rock_offset: 0,
        rock_top: 3,
        shaft: vec![0, 0, 0, 0b1111111],
        shaft_height: 3,
    };

    event_loop(
        &mut state,
        std::iter::repeat(s)
            .map(|s| s.chars().map(|c| c == '<'))
            .flatten(),
        1000000000000,
    );

    //println!("{}", state);
    //println!("{:?}", state.shaft_height - 3);
}
