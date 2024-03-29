fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut first: i32 = 0;
    let mut second: i32 = 0;

    for line in common::get_problem_lines(2022, 2) {
        let b = line.as_bytes();
        first += (((b[2] - b[0] + 2) % 3) * 3 + (b[2] - 87)) as i32;
        second += ((b[2] - 88) * 3 + ((b[0] + b[2] - 151) % 3 + 1)) as i32;
    }

    println!("{:?} {:?}", first, second);
    Ok(())
}
