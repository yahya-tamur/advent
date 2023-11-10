fn count_trailing_zeroes(z: u64) -> u64 {
    let mut c = 0;
    if z & 0xAAAAAAAAAAAAAAAAu64 != 0 {
        c |= 1;
    }
    if z & 0xCCCCCCCCCCCCCCCCu64 != 0 {
        c |= 2;
    }
    if z & 0xF0F0F0F0F0F0F0F0u64 != 0 {
        c |= 4;
    }
    if z & 0xFF00FF00FF00FF00u64 != 0 {
        c |= 8;
    }
    if z & 0xFFFF0000FFFF0000u64 != 0 {
        c |= 16;
    }
    if z & 0xFFFFFFFF00000000u64 != 0 {
        c |= 32;
    }
    c
}

fn ascii_to_small(b: u8) -> u8 {
    if b >= 97 {
        b - 96
    } else {
        b - 65 + 27
    }
}

fn first(it: impl Iterator<Item = String>) -> u64 {
    let mut sum = 0;
    for line in it {
        let bytes = line.as_bytes();
        let (fst, snd) = bytes.split_at(bytes.len() / 2);
        let fst = fst.iter().map(|&x| ascii_to_small(x)).collect::<Vec<u8>>();
        let snd = snd.iter().map(|&x| ascii_to_small(x)).collect::<Vec<u8>>();
        let (mut f_map, mut s_map) = (0u64, 0u64);
        for f in fst {
            f_map |= 1 << f;
        }
        for s in snd {
            s_map |= 1 << s;
        }
        sum += count_trailing_zeroes(f_map & s_map)
    }
    sum
}

fn second(it: impl Iterator<Item = String>) -> u64 {
    let mut sum = 0;
    let mut acc: u64 = u64::MAX;
    let mut ix = 0;
    for line in it {
        let sack = line
            .as_bytes()
            .iter()
            .map(|&x| ascii_to_small(x))
            .collect::<Vec<u8>>();
        let mut sack_map: u64 = 0;
        for s in sack {
            sack_map |= 1 << s;
        }
        acc &= sack_map;
        ix += 1;
        if ix == 3 {
            sum += count_trailing_zeroes(acc);
            acc = u64::MAX;
            ix = 0;
        }
    }
    sum
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("{}", first(common::get_problem_lines(2022, 3)));
    println!("{}", second(common::get_problem_lines(2022, 3)));
    Ok(())
}
