fn md5(s: String) {
    let mut byts = s.into_bytes();
    let o_len = byts.len();
    byts.push(0x80);
    if (o_len + 1) % 64 != 56 {
        byts.resize((((o_len + 9) / 64) + 1) * 64 - 8, 0);
    }
    byts.extend(u64::to_le_bytes(u64::try_from(o_len).unwrap()));
    println!("{:x?}", byts);
}

fn main() {
    println!("part 1: {}", common::get_problem(2016, 5));
    md5("abc".to_string());
}
