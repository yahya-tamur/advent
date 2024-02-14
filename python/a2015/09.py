from problem import gpl
from collections import defaultdict
import heapq as hq

names = dict()

con = defaultdict(set)
wht = dict()

for line in gpl():
    a, _, b, _, d = line.split(' ')
    for c in (a, b):
        if c not in names:
            names[c] = len(names)
    a, b = names[a], names[b]
    con[a].add(b)
    con[b].add(a)
    wht[(a,b)] = int(d)
    wht[(b,a)] = int(d)

def search(c):
    active = [(0, i, 1 << i) for i in range(len(names))]

    hq.heapify(active)

    while active:
        steps, loc, items = hq.heappop(active)

        if items == (1 << len(names)) - 1:
            return c*steps
            break

        for dst in con[loc]:
            if (1 << dst) & items == 0:
                hq.heappush(active, (steps + c*wht[(loc, dst)], dst, items | (1 << dst)))

print(f"part 1: {search(1)}")
print(f"part 2: {search(-1)}")

