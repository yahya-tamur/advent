from problem import gpl
from collections import defaultdict

con = defaultdict(list)
pon = set()

for line in gpl():
    l, rr = line.split(' <-> ')
    pon.add(l)
    for r in rr.split(', '):
        pon.add(r)
        con[l].append(r)
        con[r].append(l)

active = ['0']
seen = set()

while active:
    a = active.pop()
    if a in seen:
        continue
    seen.add(a)
    for a_ in con[a]:
        active.append(a_)

print(f"part 1: {len(seen)}")

p2 = 0
while pon:
    p2 += 1
    active = [next(iter(pon))]
    while active:
        a = active.pop()
        if a not in pon:
            continue
        pon.remove(a)
        for a_ in con[a]:
            active.append(a_)


print(f"part 2: {p2}")
