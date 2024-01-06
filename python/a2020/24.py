from problem import gpl
from collections import defaultdict

moves = {'e': 1, 'w': -1, 'ne': 1j, 'sw': -1j, 'nw': -1+1j, 'se': 1-1j}

def parse(s):
    i, loc = 0, 0
    while i < len(s):
        i_ = i + (1 if s[i] in 'ew' else 2)
        i, loc = i_, loc + moves[s[i:i_]]
    return loc

flipped = set()
for s in gpl(): flipped ^= {parse(s)}

print(f"part 1: {len(flipped)}")

for _ in range(100):
    hits = defaultdict(int)
    for f in flipped:
        for v in moves.values():
            hits[f+v] += 1
    flipped = {k for k, v in hits.items() if v == 2 or k in flipped and v == 1}

print(f"part 2: {len(flipped)}")
