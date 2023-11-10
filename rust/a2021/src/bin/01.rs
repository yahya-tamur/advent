fn main() {
    println!(
        "part 1: {}",
        common::get_problem_lines(2021, 1)
            .map(|l| l.parse::<i32>().unwrap())
            .collect::<Vec<i32>>()
            .windows(2)
            .filter(|s| s[0] < s[1])
            .count()
    );
    println!(
        "part 2: {}",
        common::get_problem_lines(2021, 1)
            .map(|l| l.parse::<i32>().unwrap())
            .collect::<Vec<i32>>()
            .windows(4)
            .filter(|s| s[0] < s[3])
            .count()
    );
}
