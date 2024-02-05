// I didn't want to just use a library, so I wrote an md5 implementation in
// python, then that wasn't fast enough to use in my answer so I eneded up using
// a library (hashlib).
// So, I wanted to write an implementation in a compiled language. This is a
// lot faster than the plain python implementation -- 0.8s instead of 2.1s,
// using hashlib.
// It was was a lot slower to write.
// Things like .chars.next().unwrap() or const fn's or wrapping_add or
// Arc::try_unwrap(results).unwrap().into_inner().unwrap()
// were annoying to work with.
use std::sync::{Arc, Mutex};
use std::thread;

const S: [u32; 64] = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9,
    14, 20, 5, 9, 14, 20, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 6, 10, 15,
    21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21,
];

// const floating point operations not supported??????
const K: [u32; 64] = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
];

fn md5(s: &str) -> [u8; 16] {
    let mut byts = s.as_bytes().to_vec();
    let o_len = byts.len();
    byts.push(0x80);
    if (o_len + 1) % 64 != 56 {
        byts.resize((((o_len + 9) / 64) + 1) * 64 - 8, 0);
    }
    byts.extend(u64::to_le_bytes(u64::try_from(o_len * 8).unwrap()));

    let mut a0: u32 = 0x67452301;
    let mut b0: u32 = 0xefcdab89;
    let mut c0: u32 = 0x98badcfe;
    let mut d0: u32 = 0x10325476;

    let mut i: usize = 0;
    while i < byts.len() {
        let mut m = [0u32; 16];
        for j in 0..16 {
            m[j] = (byts[i + j * 4] as u32)
                + ((byts[i + j * 4 + 1] as u32) << 8)
                + ((byts[i + j * 4 + 2] as u32) << 16)
                + ((byts[i + j * 4 + 3] as u32) << 24);
        }
        let mut a: u32 = a0;
        let mut b: u32 = b0;
        let mut c: u32 = c0;
        let mut d: u32 = d0;

        for j in 0..64 {
            let (f, g): (u32, usize) = match j {
                0..=15 => ((b & c) | (!b & d), j),
                16..=31 => ((b & d) | (!d & c), (5 * j + 1) & 15),
                32..=47 => (b ^ c ^ d, (3 * j + 5) & 15),
                48..=63 => (c ^ (b | !d), 7 * j & 15),
                _ => panic!(),
            };
            let ff = f.wrapping_add(a.wrapping_add(K[j].wrapping_add(m[g])));
            a = d;
            d = c;
            c = b;
            b = b.wrapping_add((ff << S[j]) | (ff >> (32 - S[j])));
        }
        a0 = a0.wrapping_add(a);
        b0 = b0.wrapping_add(b);
        c0 = c0.wrapping_add(c);
        d0 = d0.wrapping_add(d);

        i += 64;
    }
    let mut ans: Vec<u8> = Vec::new();
    ans.extend(a0.to_le_bytes());
    ans.extend(b0.to_le_bytes());
    ans.extend(c0.to_le_bytes());
    ans.extend(d0.to_le_bytes());
    ans.try_into().unwrap()
}

// Ok could be better
const NUM_THREADS: usize = 20;
const SEARCH_PER_THREAD: usize = 2_000_000;

fn main() {
    let inp: String = common::get_problem(2016, 5).trim().to_string();
    let results: Arc<Mutex<Vec<(usize, u16)>>> = Arc::new(Mutex::new(Vec::new()));
    let mut threads: Vec<std::thread::JoinHandle<()>> = Vec::new();

    for i in 0..NUM_THREADS {
        let res = Arc::clone(&results);
        let inp = inp.clone();
        threads.push(thread::spawn(move || {
            for j in (i * SEARCH_PER_THREAD)..((i + 1) * SEARCH_PER_THREAD) {
                let s = md5(&format!("{}{}", inp, j));
                if s[0] == 0 && s[1] == 0 && s[2] >> 4 == 0 {
                    let mut r = res.lock().unwrap();
                    r.push((j, ((s[2] as u16) << 8) | ((s[3] as u16) & 0xff)));
                }
            }
        }));
    }
    for jh in threads.into_iter() {
        jh.join().unwrap();
    }

    let mut results: Vec<(usize, u16)> = Arc::try_unwrap(results).unwrap().into_inner().unwrap();

    results.sort();

    let results: Vec<u16> = results.into_iter().map(|(_, b)| b).collect();

    let mut p1 = String::new();
    for r in &results[..8] {
        p1 += &format!("{:x?}", r >> 8);
    }
    println!("part 1: {}", p1);

    let mut left: u16 = 0xFF;
    let mut p2: Vec<char> = vec!['x'; 8];
    for r in &results {
        if ((1 << (r >> 8)) & left) != 0 {
            p2[(r >> 8) as usize] = format!("{:x?}", ((r >> 4) & 15)).chars().next().unwrap();

            left ^= 1 << (r >> 8);
        }
    }
    let p2: String = p2.into_iter().collect();
    println!("part 2: {}", p2);
}
