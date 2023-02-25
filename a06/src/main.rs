use std::collections::VecDeque;
use std::fs;

//set to 4 for part 1
const DIST: u8 = 14;

fn bitcount(mut u : u32) -> u32 {
  let mut count = 0;
  while u != 0 {
    count += 1;
    u = u & (u - 1);
  }
  count
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
  let input = fs::read_to_string("input.txt").unwrap();
  let bytes = input.as_bytes();
  let mut mask = 0u32;
  let mut queue: VecDeque<u8> = VecDeque::new();
  for (i, b) in bytes.iter().enumerate() {
    let b = *b - b'a';
    mask ^= 1 << b;
    queue.push_back(b);
    if queue.len() == DIST.into() {
      if bitcount(mask) == DIST.into() {
        println!("{}", i+1);
        return Ok(());
      }
      let q = queue.pop_front().unwrap();
      mask ^= 1 << q;
    }
  }
  Ok(())
}
