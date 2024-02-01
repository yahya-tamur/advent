from problem import gp
from knot_hash import knot_hash

from collections import defaultdict

p1 = 0

inp = gp().strip()
grid = set()
for i in range(128):
    for j, n in enumerate(knot_hash(f'{inp}-{i}')):
        for k in range(8):
            if n & (1 << (7 - k)):
                grid.add(i*1j + j*8 + k)

print(f"part 1: {len(grid)}")

p2 = 0
while grid:
    p2 += 1
    active = [next(iter(grid))]
    while active:
        a = active.pop()
        if a not in grid:
            continue
        grid.remove(a)
        for a_ in {a+d for d in [1,-1,1j,-1j]}:
            active.append(a_)

print(f"part 2: {p2}")
