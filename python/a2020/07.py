from common import gpl
from collections import defaultdict

rules = dict()
corules = defaultdict(set)

for line in gpl():
    left = line[:line.find('bag')-1]
    right = list()
    if line.find('no other bags') == -1:
        for p in line[line.find('contain') + 8:].split(', '):
            r = p.split(' ')
            right.append((int(r[0]), f"{r[1]} {r[2]}"))
            corules[f"{r[1]} {r[2]}"].add(left)
    rules[left] = right

active = ['shiny gold']
counted = set()
while active:
    a = active.pop()
    if a in counted:
        continue
    counted.add(a)
    for b in corules[a]:
        active.append(b)

print(f"part 1: {len(counted - {'shiny gold'})}")

active = [(1, 'shiny gold')]
part2 = 0
while active:
    [n, bag] = active.pop()
    part2 += n
    for (m, bag_) in rules[bag]:
        active.append((n*m, bag_))

print(f"part 2: {part2 - 1}")


