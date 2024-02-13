from problem import gpl
from collections import deque

grid = dict()
start = None
maxnum = 0

for i, line in enumerate(gpl()):
    for j, c in enumerate(line):
        if c != '#':
            grid[i+1j*j] = c
        if c == '0':
            start = i+1j*j
        if c.isnumeric():
            maxnum = max(maxnum, int(c))

active = deque([(0, start, 0)])
seen = set()

p1, p2 = None, None

while (p1 is None) or (p2 is None):
    steps, loc, items = active.popleft()

    if (loc, items) in seen:
        continue
    seen.add((loc, items))

    # It's convenient that the start item is named 0 here.
    if p1 is None and items >= (1 << (maxnum + 1)) - 2:
        p1 = steps

    if p2 is None and items == (1 << (maxnum + 1)) - 1 and loc == start:
        p2 = steps

    for loc_ in (loc+d for d in (1,-1,1j,-1j) if loc+d in grid):
        items_ = items
        if (c := grid[loc_]).isnumeric():
            items_ |= 1 << int(c)
        active.append((steps+1, loc_, items_))

print(f"part 1: {p1}")
print(f"part 2: {p2}")
