use reqwest::blocking::Client;
use std::fs;
use std::io::{prelude::*, BufReader};
use std::path;

//add automatic submitting?

fn problem_dir(year: i32) -> String {
    format!("../inputs/a{}", year)
}

fn problem_file(year: i32, day: i32) -> String {
    format!("{}/{}.txt", problem_dir(year), day)
}

fn download_problem(year: i32, day: i32) {
    let session = fs::read_to_string("../session.txt")
        .expect("Couldn't find session.txt in the parent directory");
    let session = format!("session={}", &session[0..session.len() - 1]);
    if !path::Path::new("../inputs").exists() {
        panic!("Couldn't find an inputs directory in your parent directory");
    }

    fs::create_dir_all(problem_dir(year)).unwrap();
    let resp = Client::new()
        .get(format!(
            "https://adventofcode.com/{}/day/{}/input",
            year, day
        ))
        .header("Cookie", session)
        .send()
        .unwrap();
    //.text()
    //.unwrap();

    if resp.status() != reqwest::StatusCode::OK {
        panic!("request failed... maybe session is expired?");
    }

    fs::write(problem_file(year, day), resp.text().unwrap()).unwrap();
}

pub fn get_problem(year: i32, day: i32) -> String {
    if !path::Path::new(&problem_file(year, day)).exists() {
        download_problem(year, day);
    }
    std::fs::read_to_string(&problem_file(year, day)).unwrap()
}

pub fn get_problem_lines(year: i32, day: i32) -> impl Iterator<Item = String> {
    if !path::Path::new(&problem_file(year, day)).exists() {
        download_problem(year, day);
    }
    let file = fs::File::open(problem_file(year, day)).unwrap();
    let reader = BufReader::new(file);
    reader.lines().map(|x| x.unwrap())
}
