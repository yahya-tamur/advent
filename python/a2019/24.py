from problem import gpl
from collections import defaultdict

def p1():
    # not good right now
    def encode(grid):
        l = [(int(z.real), int(z.imag)) for z in grid if grid[z] == 1]
        l.sort()
        return tuple(l)

    grid = {i+j*1j: int(c == '#') for i, line in enumerate(gpl()) for j, c in enumerate(line)}

    seen = set()
    for _ in range(200):
        eg = encode(grid)
        if eg in seen:
            return sum((2 ** (5*i + j) for i in range(5) for j in range(5) if grid[i+1j*j]))
        seen.add(eg)

        hits = {z: 0 for z in grid}
        for bug in grid:
            for d in [1, -1, 1j, -1j]:
                if bug + d in grid and grid[bug+d] == 1:
                    hits[bug] += 1
        for x, hx in hits.items():
            if (grid[x] == 1 and hx == 1) or (grid[x] == 0 and hx in [1,2]):
                hits[x] = 1
            else:
                hits[x] = 0
        grid = hits

print(f"part 1: {p1()}")

def p2():
    sides = list()
    for r in range(25):
        side = list()
        if r == 12:
            sides.append([])
            continue
        for p in [-5,5]:
            if r+p in range(25):
                side.append((r+p,0))
        if r % 5 != 0:
            side.append((r-1,0))
        if r % 5 != 4:
            side.append((r+1,0))
        sides.append([p for p in side if p[0] != 12])

    for z in [zip(range(0,5),[7]*5), zip(range(0,25,5),[11]*5), \
            zip(range(4,25,5),[13]*5), zip(range(20,25),[17]*5)]:
        for i, j in z:
            sides[i].append((j,-1))
            sides[j].append((i,1))

    grid = defaultdict(lambda:[0 for _ in range(25)])

    for i, line in enumerate(gpl()):
        for j, c in enumerate(line):
            if c == '#':
                grid[0][5*i+j] = 1

    for _ in range(200):
        hits = defaultdict(lambda:[0 for _ in range(25)])
        for height, line in grid.items():
            for i in range(25):
                if line[i]:
                    for pos, dheight in sides[i]:
                        hits[height+dheight][pos] += 1
        for height in hits.keys():
            for i in range(25):
                if (grid[height][i] == 1 and hits[height][i] == 1) or \
                        (grid[height][i] == 0 and hits[height][i] in [1,2]):
                    hits[height][i] = 1
                else:
                    hits[height][i] = 0
        grid = hits
    return sum((sum(l) for l in grid.values()))
print(f"part 2: {p2()}")
