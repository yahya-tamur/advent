from problem import get_problem_lines
from collections import deque

# type = 'b' (broadcast), '%' (flip-flop), '&' (conjunction)
# name -> (type, list of modules to send)
mods = dict()

for line in get_problem_lines():
    mods[line[1:line.find(' -> ')]] = (line[0], line[line.find(' -> ')+4:].split(', '))

for line in get_problem_lines():
    for x in line[line.find(' -> ')+4:].split(', '):
        if x not in mods:
            mods[x] = (' ', [])

conjs = {mod: len([1 for y_info in mods.values() if mod in y_info[1]]) \
        for mod, info in mods.items() if info[0] == '&'}

def copystate(s):
    return ({x for x in s[0]}, {x:{ys for ys in y} for x,y in s[1].items()})

# state is a set and a dict.
# the set has 'ab' for a flip module ab, iff ab high
# for a con module ab, dict[ab] is the set of on inputs
init = (set(), {c: set() for c, info in mods.items() if info[0] == '&'})

# low = False, high = True
# returns (high, low, state_)
def pushbutton(state):
    state_ = copystate(state)
    diff = {True: 0, False: 0}
    signals = deque([('roadcaster', 0, 'button')])
    while signals:
        s, height, sender = signals.popleft()
        diff[height] += 1
        match mods[s][0]:
            case 'b':
                for x in mods[s][1]:
                    signals.append((x, height, s))
            case '%':
                if not height:
                    if s in state_[0]:
                        state_[0].remove(s)
                    else:
                        state_[0].add(s)
                    for x in mods[s][1]:
                        signals.append((x, s in state_[0], s))
            case '&':
                if height:
                    state_[1][s].add(sender)
                else:
                    state_[1][s].discard(sender)
                for x in mods[s][1]:
                    signals.append((x,len(state_[1][s]) != conjs[s],s))
    return diff[True], diff[False], state_

highs, lows, state = 0, 0, init
for _ in range(1000):
    h, l, state = pushbutton(state)
    highs += h
    lows += l
print(f"part 1: {highs*lows}")

# I wrote this after studying the graph with pyvis network.

nums = list()
for start in mods['roadcaster'][1]:
    (a, b) = mods[start][1]
    center = a if mods[a][0] == '&' else b
    chain = start
    num = 1
    m = 2
    # weird way to write the loop
    while len(chain := [n for n in mods[chain][1] if mods[n][0] == '%']) > 0:
        chain = chain[0]
        if center in mods[chain][1]:
            num += m
        m *= 2
    nums.append(num)

from math import lcm
print(f"part 2: {lcm(*nums)}")

