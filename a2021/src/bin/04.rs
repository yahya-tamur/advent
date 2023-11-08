use std::collections::HashSet;

fn parse() -> (Vec<i16>, Vec<[i16; 25]>) {
    let s = common::get_problem(2021, 4);
    let mut lines = s.lines();
    let numbers = lines
        .next()
        .unwrap()
        .split(',')
        .map(|s| s.parse().unwrap())
        .collect::<Vec<i16>>();
    let mut boards: Vec<[i16; 25]> = vec![];
    while lines.next().is_some() {
        let mut ans: Vec<i16> = vec![];
        for _ in 0..5 {
            ans.extend(
                lines
                    .next()
                    .unwrap()
                    .split(' ')
                    .filter(|s| !s.is_empty())
                    .map(|s| s.parse::<i16>().unwrap()),
            );
        }
        boards.push(ans.try_into().unwrap());
    }
    (numbers, boards)
}

fn part1(numbers: &Vec<i16>, boards: &[[i16; 25]]) -> i64 {
    let mut current_matches: Vec<[bool; 25]> = boards.iter().map(|_| [false; 25]).collect();
    let mut updates: [Vec<(usize, usize)>; 100] = vec![Vec::new(); 100].try_into().unwrap();
    for (i, b) in boards.iter().enumerate() {
        for j in 0..25 {
            updates[b[j] as usize].push((i, j));
        }
    }
    for &n in numbers {
        for &(board, index) in &updates[n as usize] {
            current_matches[board][index] = true;
            let row = index / 5;
            let col = index % 5;
            if (current_matches[board][row * 5]
                && current_matches[board][row * 5 + 1]
                && current_matches[board][row * 5 + 2]
                && current_matches[board][row * 5 + 3]
                && current_matches[board][row * 5 + 4])
                || (current_matches[board][col]
                    && current_matches[board][col + 5]
                    && current_matches[board][col + 10]
                    && current_matches[board][col + 15]
                    && current_matches[board][col + 20])
            {
                let mut sum = 0;
                for i in 0..25 {
                    if !current_matches[board][i] {
                        sum += boards[board][i];
                    }
                }
                return (sum as i64) * (n as i64);
            }
        }
    }
    panic!("nobody won");
}

fn part2(numbers: &Vec<i16>, boards: &Vec<[i16; 25]>) -> i64 {
    let mut current_matches: Vec<[bool; 25]> = boards.iter().map(|_| [false; 25]).collect();
    let mut updates: [HashSet<(usize, usize)>; 100] = vec![HashSet::new(); 100].try_into().unwrap();
    let mut gamers: HashSet<usize> = HashSet::from_iter(0..(boards.len()));
    for (i, b) in boards.iter().enumerate() {
        for j in 0..25 {
            updates[b[j] as usize].insert((i, j));
        }
    }
    let mut to_remove: HashSet<usize> = HashSet::new();
    for &n in numbers {
        for &(board, index) in &updates[n as usize] {
            current_matches[board][index] = true;
            let row = index / 5;
            let col = index % 5;
            if (current_matches[board][row * 5]
                && current_matches[board][row * 5 + 1]
                && current_matches[board][row * 5 + 2]
                && current_matches[board][row * 5 + 3]
                && current_matches[board][row * 5 + 4])
                || (current_matches[board][col]
                    && current_matches[board][col + 5]
                    && current_matches[board][col + 10]
                    && current_matches[board][col + 15]
                    && current_matches[board][col + 20])
            {
                if gamers.len() > 1 {
                    gamers.remove(&board);
                    to_remove.insert(board);
                } else {
                    let mut sum = 0;
                    for i in 0..25 {
                        if !current_matches[board][i] {
                            sum += boards[board][i];
                        }
                    }
                    return (sum as i64) * (n as i64);
                }
            }
        }
        for &board in to_remove.iter() {
            for i in 0..25 {
                updates[boards[board][i] as usize].remove(&(board, i));
            }
        }
        to_remove.clear();
    }
    panic!("nobody won");
}

fn main() {
    let (numbers, boards) = parse();
    println!("part 1: {}", part1(&numbers, &boards));
    println!("part 2: {}", part2(&numbers, &boards));
}
