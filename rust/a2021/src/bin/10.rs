fn main() {
    let mut part1 = 0;
    let mut part2: Vec<u64> = Vec::new();
    'll: for line in common::get_problem_lines(2021, 10) {
        let mut stack: Vec<u8> = Vec::new();
        for c in line.bytes() {
            match c {
                b'(' => stack.push(b'('),
                b'[' => stack.push(b'['),
                b'{' => stack.push(b'{'),
                b'<' => stack.push(b'<'),
                b')' => {
                    if stack.pop() != Some(b'(') {
                        part1 += 3;
                        continue 'll;
                    }
                }
                b']' => {
                    if stack.pop() != Some(b'[') {
                        part1 += 57;
                        continue 'll;
                    }
                }
                b'}' => {
                    if stack.pop() != Some(b'{') {
                        part1 += 1197;
                        continue 'll;
                    }
                }
                b'>' => {
                    if stack.pop() != Some(b'<') {
                        part1 += 25137;
                        continue 'll;
                    }
                }
                _ => panic!("other character"),
            }
        }
        let mut ans = 0;
        for c in stack.iter().rev() {
            ans = ans * 5
                + match c {
                    b'[' => 2,
                    b'(' => 1,
                    b'{' => 3,
                    b'<' => 4,
                    _ => panic!("A"),
                }
        }
        part2.push(ans);
    }
    println!("part 1: {}", part1);
    part2.sort();
    println!("part 2: {}", part2[part2.len() / 2]);
}
