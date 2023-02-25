use std::cmp::Reverse;
use std::fs::File;
use std::io::{prelude::*, BufReader};
use std::collections::BinaryHeap;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open("input.txt")?;
    let reader = BufReader::new(file);
    let mut heap = BinaryHeap::from([Reverse(0);3]);
    let mut acc: i32 = 0;

    for line in reader.lines().map(|a| a.unwrap()) {
      if line.is_empty() {
        heap.push(Reverse(acc));
        heap.pop();
        acc = 0;
      } else {
        acc += line.parse::<i32>()?;
      }
    }
  heap.push(Reverse(acc));
  heap.pop();
  let v: Vec<i32> = heap.into_sorted_vec().into_iter().map(|a| a.0).collect();
  println!("{:?}", v);
  println!("{:?}", v.iter().sum::<i32>());
  Ok(())
}
