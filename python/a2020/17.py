add = [lambda t0, t1: (t0[0]+t1[0],t0[1]+t1[1],t0[2]+t1[2]), \
        lambda t0, t1: (t0[0]+t1[0],t0[1]+t1[1],t0[2]+t1[2],t0[3]+t1[3])]

surr = [{(a, b, c) for a in range(-1,2) for b in range(-1,2) \
        for c in range(-1,2) if not (a, b, c) == (0, 0, 0)}, \
        {(a, b, c, d) for a in range(-1,2) for b in range(-1,2) \
        for c in range(-1,2) for d in range(-1,2) \
        if not (a, b, c, d) == (0, 0, 0, 0)}]

from common import gpl

map = [{(i, j, 0) for i, line in enumerate(gpl()) for j, c in enumerate(line) \
        if c == '#'}, \
    {(i, j, 0, 0) for i, line in enumerate(gpl()) for j, c in enumerate(line) \
        if c == '#'}]

from collections import defaultdict

for _ in range(6):
    hits = [defaultdict(int), defaultdict(int)]
    for p in range(2):
        for m in map[p]:
            for s in surr[p]:
                hits[p][add[p](m,s)] += 1
        map[p] = {m for m, c in hits[p].items() if c == 3 or (c == 2 and m in map[p])}

print(f"part 1: {len(map[0])}")
print(f"part 2: {len(map[1])}")

