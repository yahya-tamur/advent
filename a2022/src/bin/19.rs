//takes a bit too long but I didn't multithread it after multithreading 16-2
//I might factor out the common parts and use that for both of these
use regex::{Match, Regex};

#[derive(Debug)]
struct Blueprint {
    ore_ore: u32,
    clay_ore: u32,
    obs_ore: u32,
    obs_clay: u32,
    geo_ore: u32,
    geo_obs: u32,
}

fn parse(input: &str) -> Vec<Blueprint> {
    let r = Regex::new(
        r"(?xs).*?
        Blueprint.*?
        ore\ robot\ costs\ (?P<o_o>\d+)\ ore.*?
        clay\ robot\ costs\ (?P<c_o>\d+)\ ore.*?
        obsidian\ robot\ costs\ (?P<ob_o>\d+)\ ore\ and\ (?P<ob_c>\d+)\ clay.*?
        geode\ robot\ costs\ (?P<g_o>\d+)\ ore\ and\ (?P<g_ob>\d+)\ obsidian.*?",
    )
    .unwrap();
    let read_to_u32 = |s: Option<Match>| s.unwrap().as_str().parse::<u32>().unwrap();
    r.captures_iter(input)
        .map(|caps| Blueprint {
            ore_ore: read_to_u32(caps.name("o_o")),
            clay_ore: read_to_u32(caps.name("c_o")),
            obs_ore: read_to_u32(caps.name("ob_o")),
            obs_clay: read_to_u32(caps.name("ob_c")),
            geo_ore: read_to_u32(caps.name("g_o")),
            geo_obs: read_to_u32(caps.name("g_ob")),
        })
        .collect()
}

#[derive(Debug, Clone)]
struct State {
    ore: u32,
    clay: u32,
    obs: u32,
    geo: u32,
    ore_robots: u32,
    clay_robots: u32,
    obs_robots: u32,
    geo_robots: u32,
    time: u32,
}

fn evaluate_blueprint(bp: &Blueprint, time_max: u32) -> u32 {
    let mut states = vec![State {
        ore: 0,
        clay: 0,
        obs: 0,
        geo: 0,
        ore_robots: 1,
        clay_robots: 0,
        obs_robots: 0,
        geo_robots: 0,
        time: 0,
    }];
    let mut max_geodes = 0;

    let ore_robots_necessary = *[bp.ore_ore, bp.geo_ore, bp.clay_ore, bp.geo_ore]
        .iter()
        .max()
        .unwrap();

    let advance = |s: &State| State {
        ore: s.ore + s.ore_robots,
        clay: s.clay + s.clay_robots,
        obs: s.obs + s.obs_robots,
        geo: s.geo + s.geo_robots,
        ore_robots: s.ore_robots,
        clay_robots: s.clay_robots,
        obs_robots: s.obs_robots,
        geo_robots: s.geo_robots,
        time: s.time + 1,
    };
    while let Some(state) = states.pop() {
        if state.time == time_max
            || state.geo
                + ((time_max - 1 - state.time) * (time_max - state.time) / 2)
                + (time_max - state.time) * state.geo_robots
                < max_geodes
        {
            if state.geo > max_geodes {
                max_geodes = state.geo;
            }
            continue;
        }

        states.push(advance(&state));
        if (state.ore >= bp.ore_ore) && state.ore_robots < ore_robots_necessary {
            let mut newstate = advance(&state);
            newstate.ore -= bp.ore_ore;
            newstate.ore_robots += 1;
            states.push(newstate);
        }
        if (state.ore >= bp.clay_ore) && state.clay_robots < bp.obs_clay {
            let mut newstate = advance(&state);
            newstate.ore -= bp.clay_ore;
            newstate.clay_robots += 1;
            states.push(newstate);
        }
        if (state.ore >= bp.obs_ore) && (state.clay >= bp.obs_clay) && state.obs_robots < bp.geo_obs
        {
            let mut newstate = advance(&state);
            newstate.ore -= bp.obs_ore;
            newstate.clay -= bp.obs_clay;
            newstate.obs_robots += 1;
            states.push(newstate);
        }
        if (state.ore >= bp.geo_ore) && (state.obs >= bp.geo_obs) {
            let mut newstate = advance(&state);
            newstate.ore -= bp.geo_ore;
            newstate.obs -= bp.geo_obs;
            newstate.geo_robots += 1;
            states.push(newstate);
        }
    }
    max_geodes
}

fn main() {
    let blueprints = parse(&std::fs::read_to_string("inputs/19.txt").unwrap());
    let mut ans = 0;
    for (i, bp) in blueprints.iter().enumerate() {
        println!("{}", i + 1);
        ans += (i as u32 + 1) * evaluate_blueprint(bp, 24);
    }
    let mut ans2 = 1;
    for (i, bp) in blueprints.iter().enumerate().take(3) {
        println!("{}", i + 1);
        ans2 *= evaluate_blueprint(bp, 32);
    }
    println!("part 1: {}", ans);
    println!("part 2: {}", ans2);
}
