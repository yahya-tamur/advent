from problem import get_problem, get_problem_lines, look
from collections import defaultdict, deque

m = defaultdict(lambda:'!')

start, end = 0, 0
for i, line in enumerate(get_problem_lines()):
    for j, c in enumerate(line):
        z = i+1j*j
        if c == '#':
            m[z] = '#'
            continue
        m[z] = '.'
        match c:
            case 'S': start = z
            case 'E': end = z

times = [0 for _ in range(len(m))]

best_noskip = len(m)
import heapq as h

seen = dict()
stack = [(0, str(start))]
while stack:
    steps, z = h.heappop(stack)
    z = complex(z)
    if z == end:
        seen[z] = steps
        best_noskip = steps
        break
    if seen.get(z, len(m)) <= steps:
        continue
    seen[z] = steps
    for z_ in (z+1, z-1, z+1j, z-1j):
        if m[z_] != '.':
            continue
        stack.append((steps + 1, str(z_)))

cheats = [0 for i in range(len(m))]
mk = list(m.keys())
for z in mk:
    for d in (1, 1j):
        if m[z] == '.' and m[z+d] == '#' and m[z+2*d] == '.' and \
                z in seen and (z+2*d) in seen:
            cheats[abs(seen[z] - seen[z+2*d]) - 2] += 1

print(f"part 1: {sum(cheats[100:])}")

d20 = set()
for d in (1, -1, 1j, -1j):
    for k in range(21):
        for l in range(k+1):
            d20.add((k-l)*d + l*d*1j)

cheats = [0 for i in range(len(m))]
for z in mk:
    for z_ in (z + d for d in d20):
        if m[z] == '.' and m[z_] == '.' and z in seen and z_ in seen \
                and seen[z_] > seen[z]:
            ln = int(abs(z_.real - z.real) + abs(z_.imag - z.imag))
            cheats[seen[z_] - seen[z] - ln] += 1

#print(f"input: {sum(cheats[50:])}")
print(f"part 2: {sum(cheats[100:])}")
