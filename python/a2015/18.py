from problem import gpl

def solve(part):
    grid = set()

    for i, line in enumerate(gpl()):
        for j, c in enumerate(line):
            if c == '#':
                grid.add(i+1j*j)

    grid_ = set()
    for _ in range(100):
        grid_.clear()
        if part == 2:
            grid_ |= {0, 99, 99j, 99+99j}
        for i in range(100):
            for j in range(100):
                z = i+1j*j
                n = len({z+d for d in (1-1j,1,1+1j,1j,-1+1j,-1,-1-1j,-1j)} & grid)
                if n == 3 or (z in grid and n == 2):
                    grid_.add(z)
        grid, grid_ = grid_, grid
    return len(grid)

print(f"part 1: {solve(1)}")
print(f"part 2: {solve(2)}")
