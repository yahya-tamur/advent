use std::collections::VecDeque;

fn main() {
    let it = common::get_problem_lines(2022, 12);
    let mut heights: Vec<Vec<u8>> = it.map(|x| x.into_bytes()).collect();
    let (n, m) = (heights.len(), heights[0].len());
    let (mut start, mut end) = ((0, 0), (0, 0));
    let mut in_progress = VecDeque::new();
    let mut distances = vec![vec![u64::MAX; m]; n];
    for (i, v) in heights.iter().enumerate() {
        for (j, b) in v.iter().enumerate() {
            match b {
                b'a' => {
                    //comment these next two lines for part 1:
                    in_progress.push_back((i, j));
                    distances[i][j] = 0;
                }
                b'S' => {
                    in_progress.push_back((i, j));
                    distances[i][j] = 0;
                    start = (i, j);
                }
                b'E' => {
                    end = (i, j);
                }
                _ => {}
            }
        }
    }
    heights[start.0][start.1] = b'a';
    heights[end.0][end.1] = b'z';
    let can_jump = |ax: usize, ay: usize, bx: usize, by: usize| {
        let d1 = heights[ax][ay] as i32;
        let d2 = heights[bx][by] as i32;
        d2 <= d1 + 1
    };
    println!("{:?} {:?}", start, end);
    loop {
        let (elx, ely) = in_progress.pop_front().unwrap();
        if elx == end.0 && ely == end.1 {
            break;
        }
        if elx > 0 && can_jump(elx, ely, elx - 1, ely) && distances[elx - 1][ely] == u64::MAX {
            distances[elx - 1][ely] = distances[elx][ely] + 1;
            in_progress.push_back((elx - 1, ely));
        }
        if elx < n - 1 && can_jump(elx, ely, elx + 1, ely) && distances[elx + 1][ely] == u64::MAX {
            distances[elx + 1][ely] = distances[elx][ely] + 1;
            in_progress.push_back((elx + 1, ely));
        }
        if ely > 0 && can_jump(elx, ely, elx, ely - 1) && distances[elx][ely - 1] == u64::MAX {
            distances[elx][ely - 1] = distances[elx][ely] + 1;
            in_progress.push_back((elx, ely - 1));
        }
        if ely < m - 1 && can_jump(elx, ely, elx, ely + 1) && distances[elx][ely + 1] == u64::MAX {
            distances[elx][ely + 1] = distances[elx][ely] + 1;
            in_progress.push_back((elx, ely + 1));
        }
    }
    println!("{:?}", distances[end.0][end.1]);
}
