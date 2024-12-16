from problem import get_problem, get_problem_lines
from math import inf

m = dict()
loc = 0
exs = 0

for i, line in enumerate(get_problem_lines()):
    for j, c in enumerate(line):
        z=i+1j*j
        m[z] = c
        if c == 'S':
            loc = z
            m[z] = '.'
        if c == 'E':
            exs = z
            m[z] = '.'

import heapq as h

seen = dict()
stack = [(0, 0, str(loc), str(1j))]
prevs = [(-1, -1)]

best = inf

ends = []

while True:
    cost, ix, loc, d = h.heappop(stack)
    loc = complex(loc)
    d = complex(d)

    if cost > best:
        break

    if loc == exs:
        if cost < best:
            best = cost
            ends.clear()
        ends.append(ix)
        continue

    if seen.get((loc, d), inf) < cost:
        continue
    seen[(loc, d)] = cost

    if m[loc+d] == '.':

        h.heappush(stack, (cost+1, len(prevs), str(loc+d), str(d)))
        prevs.append((ix, loc))

    for d_ in (d*1j, -d*1j):
        h.heappush(stack, (cost+1000, len(prevs), str(loc), str(d_)))
        prevs.append((ix, loc))

seen = {exs}
for ix in ends:
    loc = exs
    while ix != -1:
        seen.add(loc)
        ix, loc = prevs[ix]
print(f"part 1: {best}")
print(f"part 2: {len(seen)}")

