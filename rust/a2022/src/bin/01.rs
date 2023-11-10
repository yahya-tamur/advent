use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut heap = BinaryHeap::from([Reverse(0); 3]);
    let mut acc: i32 = 0;

    for line in common::get_problem_lines(2022, 1) {
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
