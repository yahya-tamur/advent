#[derive(Debug, PartialEq, Eq, Clone, Copy)]
enum SNode {
    Num(u8),
    LBra,
    Comma,
    RBra,
}

type SVec = Vec<SNode>;

fn tosn(s: &str) -> SVec {
    s.chars()
        .map(|c| match c {
            '[' => SNode::LBra,
            ',' => SNode::Comma,
            ']' => SNode::RBra,
            c => SNode::Num(c.to_digit(10).unwrap() as u8),
        })
        .collect::<Vec<SNode>>()
}

/*
fn psn(s: &SVec) {
    for c in s {
        match c {
            SNode::LBra => print!("["),
            SNode::Comma => print!(","),
            SNode::RBra => print!("]"),
            SNode::Num(n) => print!("{n}"),
        }
    }
    println!("");
}
*/

fn explode(sn: &mut SVec) -> bool {
    let mut depth = 0;
    let mut k = None;
    for i in 0..sn.len() {
        if sn[i] == SNode::LBra {
            depth += 1;
        } else if sn[i] == SNode::RBra {
            depth -= 1;
        } else if depth > 4 {
            if let SNode::Num(l) = sn[i] {
                if let SNode::Num(r) = sn[i + 2] {
                    k = Some((i, l, r));
                    break;
                }
            }
        }
    }
    if let Some((i, l, r)) = k {
        for p in sn[..i].iter_mut().rev() {
            if let SNode::Num(v) = *p {
                *p = SNode::Num(v + l);
                break;
            }
        }
        for p in &mut sn[i + 3..] {
            if let SNode::Num(v) = *p {
                *p = SNode::Num(v + r);
                break;
            }
        }
        sn[i - 1] = SNode::Num(0);
        sn.drain(i..=i + 3);
        true
    } else {
        false
    }
}

fn split(sn: &mut SVec) -> bool {
    let mut k = None;
    for (i, p) in sn.iter().enumerate() {
        if let &SNode::Num(v) = p {
            if v >= 10 {
                k = Some((i, v));
                break;
            }
        }
    }
    if let Some((i, v)) = k {
        let l = v / 2;
        let r = v - l;
        sn.splice(
            i..=i,
            vec![
                SNode::LBra,
                SNode::Num(l),
                SNode::Comma,
                SNode::Num(r),
                SNode::RBra,
            ],
        );
        true
    } else {
        false
    }
}

fn add(sn1: &SVec, sn2: &SVec) -> SVec {
    let mut a: Vec<SNode> = vec![SNode::LBra];
    a.extend(sn1);
    a.push(SNode::Comma);
    a.extend(sn2);
    a.push(SNode::RBra);
    a
}

fn simplify(sn: &mut SVec) {
    while explode(sn) || split(sn) {}
}

fn magnitude(sn: &SVec) -> u32 {
    let mut k = 1;
    let mut ans = 0;
    for c in sn {
        match c {
            SNode::LBra => k *= 3,
            SNode::Comma => {
                k /= 3;
                k *= 2;
            }
            SNode::RBra => k /= 2,
            SNode::Num(c) => ans += (*c as u32) * k,
        }
    }
    ans
}

fn main() {
    let mut lines = vec![];
    for line in common::get_problem_lines(2021, 18) {
        lines.push(tosn(&line));
    }

    let mut sn = lines[0].clone();
    for sn_ in &lines[1..] {
        sn = add(&sn, sn_);
        simplify(&mut sn);
    }
    println!("part 1: {}", magnitude(&sn));
    explode(&mut sn);

    let mut ans = 0;
    for i in 0..lines.len() {
        for j in 0..lines.len() {
            if i == j {
                continue;
            }
            let mut sn = add(&lines[i], &lines[j]);
            simplify(&mut sn);
            ans = ans.max(magnitude(&sn));
        }
    }
    println!("part 2: {}", ans);
}
