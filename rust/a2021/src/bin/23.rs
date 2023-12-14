use common::dfsrunner::{run, MessageSender, RunParameters};
use std::collections::BinaryHeap;
use std::fmt;

#[derive(Debug, Default, PartialEq, Eq, PartialOrd, Ord, Clone, Copy, Hash)]
struct State {
    hallway: [u8; 11], //can save 4 more bytes :(
    rooms: [[u8; 2]; 4],
}

impl State {
    fn new() -> State {
        let lines = common::get_problem_lines(2021, 23).collect::<Vec<String>>();
        let mut s: State = Default::default();
        for room in 0..4 {
            s.rooms[room][1] = lines[2].as_bytes()[2 * room + 3] - b'A' + 1;
            s.rooms[room][0] = lines[3].as_bytes()[2 * room + 3] - b'A' + 1;
        }
        s
    }
    fn test() -> State {
        let mut s: State = Default::default();
        s.rooms[0] = [1, 2];
        s.rooms[1] = [4, 3];
        s.rooms[2] = [3, 2];
        s.rooms[3] = [1, 4];
        s
    }
    fn ok(&self) -> bool {
        for i in 0..4 {
            for k in 0..2 {
                if self.rooms[i][k] != i as u8 + 1 {
                    return false;
                }
            }
        }
        true
    }
}

impl fmt::Display for State {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let to_u8 = |c: u8| -> char {
            match c {
                0 => '.',
                c => (c + b'A' - 1) as char,
            }
        };

        for room in &self.rooms {
            if room.len() > 2 {
                writeln!(f, "Overfull Room!")?;
            }
        }
        write!(f, "#############\n#")?;
        for c in &self.hallway {
            write!(f, "{}", to_u8(*c))?;
        }
        write!(f, "#\n###")?;
        for room in &self.rooms {
            write!(f, "{}#", to_u8(room[1]))?;
        }
        write!(f, "##\n  #")?;
        for room in &self.rooms {
            write!(f, "{}#", to_u8(room[0]))?;
        }
        writeln!(f, "\n  #########\n")
    }
}

const ROOMS: [usize; 4] = [2, 4, 6, 8];

fn costs(c: u8) -> i32 {
    match c {
        1 => 1,
        2 => 10,
        3 => 100,
        4 => 1000,
        _ => panic!("aaa!"),
    }
}

fn part1(s: State) -> i32 {
    // let mut prevs: HashMap<State, (i32, State)> = HashMap::new();
    let mut heap = BinaryHeap::new();
    heap.push((0, s));
    loop {
        let (cost, s) = heap.pop().unwrap();
        //println!("{} {} {}", s, cost, s.ok());
        if s.ok() {
            /*   let mut current = s;
            println!("{:?}", prevs.get(&current));
            println!("#######################################################");
            while let Some((dcost, current_)) = prevs.get(&current) {
                println!("{}\n{}", dcost, current_);
                current = *current_;
                if current.ok() {
                    return -cost;
                }
            }*/
            return -cost;
        }
        // room out to hallway
        for room in 0..4 {
            if s.rooms[room][0] == 0 {
                continue;
            }
            let height = if s.rooms[room][1] != 0 { 1 } else { 0 };
            if s.rooms[room][0] == room as u8 + 1
                && (height == 0 || s.rooms[room][1] == room as u8 + 1)
            {
                continue;
            }
            let mut j = (ROOMS[room] + 1) as usize;
            while j < 11 && s.hallway[j] == 0 {
                if j % 2 == 1 || j == 0 || j == 10 {
                    let mut s_ = s;
                    s_.hallway[j] = s.rooms[room][height];
                    s_.rooms[room][height] = 0;
                    heap.push((
                        cost - costs(s.rooms[room][height])
                            * ((j - ROOMS[room]) as i32 + (2 - (height as i32))),
                        s_,
                    ));
                    /*prevs.insert(
                        s_,
                        (
                            costs(s.rooms[room][height])
                                * ((j - ROOMS[room]) as i32 + (2 - (height as i32))),
                            s,
                        ),
                    );*/
                }
                j += 1
            }
            let mut j = (ROOMS[room] - 1) as usize;
            while j < 11 && s.hallway[j] == 0 {
                if j % 2 == 1 || j == 0 || j == 10 {
                    let mut s_ = s;
                    s_.hallway[j] = s.rooms[room][height];
                    s_.rooms[room][height] = 0;
                    heap.push((
                        cost - costs(s.rooms[room][height])
                            * ((ROOMS[room] - j) as i32 + (2 - (height as i32))),
                        s_,
                    ));
                    /*prevs.insert(
                        s_,
                        (
                            costs(s.rooms[room][height])
                                * ((ROOMS[room] - j) as i32 + (2 - (height as i32))),
                            s,
                        ),
                    );*/
                }
                j -= 1
            }
        }
        // hallway into room
        'outer: for j in 0..11 {
            if s.hallway[j] == 0 {
                continue;
            }
            let room = (s.hallway[j] - 1) as usize;
            if s.rooms[room][1] != 0 {
                continue;
            }
            let height = if s.rooms[room][0] != 0 { 1 } else { 0 }; //NOT the same as height above.
            if height == 1 && s.rooms[room][0] != s.hallway[j] {
                continue;
            }
            if j > ROOMS[room] {
                for i in (ROOMS[room] + 1)..j {
                    if s.hallway[i] != 0 {
                        continue 'outer;
                    }
                }
            } else {
                for i in (j + 1)..ROOMS[room] {
                    if s.hallway[i] != 0 {
                        continue 'outer;
                    }
                }
            }
            let mut s_ = s;
            s_.rooms[room][height] = s.hallway[j];
            s_.hallway[j] = 0;
            heap.push((
                cost - costs(s.hallway[j])
                    * ((ROOMS[room] as i32 - j as i32).abs() + (2 - (height as i32))),
                s_,
            ));
            /*prevs.insert(
                s_,
                (
                    costs(s.hallway[j])
                        * ((ROOMS[room] as i32 - j as i32).abs() + (2 - (height as i32))),
                    s,
                ),
            );*/
        }
    }
}

fn main() {
    let s = State::new();
    println!("{:?}", s);
    println!("{}", s);
    let s = State::test();
    println!("{:?}", s);
    println!("{}", s);
    println!("{}", std::mem::size_of::<State>());
    println!("{}", part1(State::new()));
}
