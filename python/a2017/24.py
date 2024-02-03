from problem import gpl
from collections import defaultdict

comps = defaultdict(list)

for i, line in enumerate(gpl()):
    (l,r) = line.split('/')
    l, r = int(l), int(r)
    comps[l].append((r,i))
    comps[r].append((l,i))

p1 = -1
p2 = (-1, -1) # len, cost
active = [(0, 0, 0, 0)]
while active:
    (used, cost, end, lng) = active.pop()
    p1 = max(p1, cost)
    p2 = max(p2, (lng, cost))
    for (r, i) in comps[end]:
        if (1 << i) & used:
            continue
        active.append((used | (1 << i), cost + end + r, r, lng + 1))

print(f"part 1: {p1}")
print(f"part 2: {p2[1]}")
