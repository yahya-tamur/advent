from problem import gpl

pl = gpl()

loc = len(pl)//2 + (len(pl[0])//2)*1j
dr = -1

grid = {i+j*1j for i, line in enumerate(pl) for j, c in enumerate(line) if c == '#'}

p1 = 0
for _ in range(10_000):
    if loc in grid:
        dr *= -1j
        grid.remove(loc)
    else:
        dr *= 1j
        grid.add(loc)
        p1 += 1
    loc += dr

print(f"part 1: {p1}")


from collections import defaultdict

loc = len(pl)//2 + (len(pl[0])//2)*1j
dr = -1

grid = defaultdict(int)
for i, line in enumerate(pl):
    for j, c in enumerate(line):
        if c == '#':
            grid[i+1j*j] = 2

p2 = 0
for _ in range(10_000_000):
    match grid[loc]:
        case 0:
            dr *= 1j
        case 2:
            dr *= -1j
        case 3:
            dr *= -1
    grid[loc] = (grid[loc] + 1) % 4
    if grid[loc] == 2:
        p2 += 1
    loc += dr

print(f"part 2: {p2}")
