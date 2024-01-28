from problem import gp
from math import floor, sqrt
from collections import defaultdict
inp = int(gp())

def p1(i):
    k = (floor(sqrt(i-1)) - 1)// 2 + 1

    j = (i - (2*k-1)**2 - 1) % (k*2)

    return k*2 - j - 1 if j < (k-1) else j + 1

print(f"part 1: {p1(inp)}")

grid = defaultdict(int)

loc = 0
grid[loc] = 1
rot = 1

while grid[loc] <= inp:
    if grid[loc + rot*1j] == 0:
        rot *= 1j
    loc += rot
    grid[loc] = sum((grid[loc+d] for d in [1,-1,1j,-1j,1+1j,1-1j,-1+1j,-1-1j]))
    
print(f"part 2: {grid[loc]}")
