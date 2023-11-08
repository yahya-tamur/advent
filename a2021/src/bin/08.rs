fn decode(line: &str) -> i32 {
    let i = line.find('|').unwrap();
    let mut incidences = [0; 7];
    for &c in line[0..i].as_bytes() {
        if (b'a'..=b'g').contains(&c) {
            incidences[(c - b'a') as usize] += 1;
        }
    }
    let fourletterword = line[0..i].split(' ').find(|s| s.len() == 4).unwrap();

    let decoded: Vec<char> = incidences
        .iter()
        .enumerate()
        .map(|(i, icd)| match icd {
            4 => 'e',
            6 => 'b',
            7 => {
                if fourletterword.find((b'a' + i as u8) as char).is_some() {
                    'd'
                } else {
                    'g'
                }
            }
            8 => {
                if fourletterword.find((b'a' + i as u8) as char).is_some() {
                    'c'
                } else {
                    'a'
                }
            }
            9 => 'f',
            _ => panic!("uhm"),
        })
        .collect();

    let mut ans = 0;
    for code in line[i + 2..].split(' ') {
        let mut decoded: Vec<char> = code.bytes().map(|c| decoded[(c - b'a') as usize]).collect();
        decoded.sort();
        let digit = match decoded.into_iter().collect::<String>().as_str() {
            "abcefg" => 0,
            "cf" => 1,
            "acdeg" => 2,
            "acdfg" => 3,
            "bcdf" => 4,
            "abdfg" => 5,
            "abdefg" => 6,
            "acf" => 7,
            "abcdefg" => 8,
            "abcdfg" => 9,
            _ => panic!("aa"),
        };
        ans = ans * 10 + digit;
    }

    ans
}

fn main() {
    let mut ans = 0;
    for line in common::get_problem_lines(2021, 8) {
        let i = line.find('|').unwrap();
        for str in line[i + 2..].split(' ') {
            let n = str.len();
            if n == 2 || n == 4 || n == 3 || n == 7 {
                ans += 1;
            }
        }
    }
    println!("part 1: {}", ans);

    println!(
        "part 2: {}",
        common::get_problem_lines(2021, 8)
            .map(|line| decode(&line))
            .sum::<i32>()
    );
}
