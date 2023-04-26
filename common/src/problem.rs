use dotenv::dotenv;
use dotenv_codegen::dotenv;
use reqwest::blocking::Client;
use std::fs;
use std::io::{prelude::*, BufReader};
use std::path::*;

fn input_dir() -> PathBuf {
    PathBuf::from(dotenv!("INPUT_DIR"))
}

fn session_file() -> PathBuf {
    PathBuf::from(dotenv!("SESSION_FILE"))
}

fn problem_dir<'a>(year: i32) -> PathBuf {
    input_dir().join(format!("a{}", year))
}

fn problem_file<'a>(year: i32, day: i32) -> PathBuf {
    problem_dir(year).join(format!("{}.txt", day))
}

fn download_problem(year: i32, day: i32) {
    if !session_file().exists() {
        panic!("Couldn't find the session file");
    }
    if !input_dir().exists() {
        panic!("Couldn't find the inputs folder");
    }
    let session = fs::read_to_string(session_file()).unwrap();
    //deletes new line at the end
    let session = format!("session={}", &session[0..session.len() - 1]);

    let resp = Client::new()
        .get(format!(
            "https://adventofcode.com/{}/day/{}/input",
            year, day
        ))
        .header("Cookie", session)
        .send()
        .unwrap();

    if resp.status() != reqwest::StatusCode::OK {
        panic!("request failed... maybe session is expired?");
    }

    fs::create_dir_all(problem_dir(year)).unwrap();
    fs::write(problem_file(year, day), resp.text().unwrap()).unwrap();
}

pub fn get_problem(year: i32, day: i32) -> String {
    dotenv().ok();
    if !problem_file(year, day).exists() {
        download_problem(year, day);
    }
    std::fs::read_to_string(problem_file(year, day)).unwrap()
}

pub fn get_problem_lines(year: i32, day: i32) -> impl Iterator<Item = String> {
    dotenv().ok();
    if !problem_file(year, day).exists() {
        download_problem(year, day);
    }
    let file = fs::File::open(problem_file(year, day)).unwrap();
    let reader = BufReader::new(file);
    reader.lines().map(|x| x.unwrap())
}
