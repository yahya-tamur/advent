from problem import gpl

grid = [[1,2,3],[4,5,6],[7,8,9]]
grid = {i+1j*j: str(n) for i, line in enumerate(grid) for j, n in enumerate(line)}

loc1 = 1+1j

# I thought this was a little silly, but then the program worked first try.
grid2 =                  {-2: '1', \
              -1j-1: '2', -1: '3', 1j-1: '4', \
    -2j: '5',   -1j: '6',  0: '7',    1j: '8', 2j: '9', \
              -1j+1: 'A',  1: 'B',  1j+1: 'C', \
                           2: 'D'}

loc2 = 0

dr = {'R': 1j, 'L': -1j, 'U': -1, 'D': 1}

p1 = ''
p2 = ''

for line in gpl():
    for c in line:
        if (loc1_ := (loc1 + dr[c])) in grid:
            loc1 = loc1_
        if (loc2_ := (loc2 + dr[c])) in grid2:
            loc2 = loc2_
    p1 += grid[loc1]
    p2 += grid2[loc2]

print(f"part 1: {p1}")
print(f"part 2: {p2}")
