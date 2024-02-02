from problem import gpl

grid = {i + 1j*j: c for i, line in enumerate(gpl()) for j, c in enumerate(line) if c != ' '}

loc = next((z for z in grid if z.real == 0))
dr = 1j

p1 = ''
p2 = 1

while True:
    try:
        loc, dr = next(( (loc+dr*d, dr*d) for d in [1,1j,-1j] if loc+dr*d in grid ))
        p2 += 1
        if grid[loc].isalpha():
            p1 += grid[loc]
    except StopIteration:
        break

print(f"part 1: {p1}")
print(f"part 2: {p2}")

