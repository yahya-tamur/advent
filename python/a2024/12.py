from problem import get_problem, get_problem_lines
from collections import defaultdict

m = defaultdict(lambda:'!')
for i, line in enumerate(get_problem_lines()):
    for j, c in enumerate(line):
        m[i+1j*j] = c

notseen = set(m.keys())

ans = 0
ans2 = 0

while notseen:
    start = notseen.pop()
    ch = m[start]
    stack = [start]
    area, perimeter = 0, 0
    sides = set()
    while stack:
        node = stack.pop()
        area += 1
        perimeter += 4
        for d in (1, -1, 1j, -1j):
            node_ = node + d
            if m[node_] != ch:
                sides.add((node, d))
                continue
            perimeter -= 1
            if node_ not in notseen:
                continue
            notseen.remove(node_)
            stack.append(node_)

    side_adj = 0
    for (node, d) in sides:
        if (node+d*1j, d) in sides:
            side_adj -= 1

    ans += area*perimeter
    ans2 += area*(len(sides) + side_adj)



print(f"part 1: {ans}")
print(f"part 2: {ans2}")
