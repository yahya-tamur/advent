from problem import gpl
from collections import defaultdict, deque

grid = defaultdict(lambda:'?')
for i, line in enumerate(gpl()):
    for j, c in enumerate(line):
        grid[(i+j*1j)] = c

N, M = len(gpl()), len(gpl()[0])

labels = defaultdict(lambda:[None, None])
map = set() # complex 
for z in list(grid.keys()): # grid size can change if we access out of bounds!
    if grid[z] == '.':
        map.add(z)
    if grid[z].isupper():
        index = 1
        if grid[z+1].isupper():
            if z.real == 0 or z.real + 2 == N:
                index = 0
            lbl = grid[z] + grid[z+1]
            if grid[z+2] == '.':
                labels[lbl][index] = z+2
            else:
                labels[lbl][index] = z-1
        if grid[z+1j].isupper():
            if z.imag == 0 or z.imag + 2 == M:
                index = 0
            lbl = grid[z] + grid[z+1j]
            if grid[z+2j] == '.':
                labels[lbl][index] = z+2j
            else:
                labels[lbl][index] = z-1j

portals = defaultdict(list)
for lbl, lbls in labels.items():
    a, b = lbls
    if b is None:
        continue
    portals[a].append((b, -1))
    portals[b].append((a, 1))

start = labels['AA'][0]
end = labels['ZZ'][0]

act = deque([(start,0)])
seen = set()

while act:
    a, n = act.popleft()

    if a not in map or a in seen:
        continue

    seen.add(a)

    if a == end:
        print(f"part 1: {n}")
        break

    for b in [a+1, a+1j, a-1, a-1j] + [x for x, _ in portals[a]]:
        act.append((b, n+1))


act = deque([(start,0,0)])
seen = set()

while act:
    a, lvl, n = act.popleft()

    if a not in map or (a,lvl) in seen or lvl < 0:
        continue

    seen.add((a,lvl))

    if a == end and lvl == 0:
        print(f"part 2: {n}")
        break

    for b, dlvl in [(a+1,0), (a+1j,0), (a-1,0), (a-1j,0)] + portals[a]:
        act.append((b, lvl + dlvl, n+1))
