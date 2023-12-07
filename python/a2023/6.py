from common import get_problem_lines
from math import sqrt, ceil

times, dists  = [[x for x in line.split(' ')[1:] if x] for line in \
         get_problem_lines(2023,6)]

def solve(n,m):
    r = sqrt(n*n - 4*m)/2
    if n % 2:
        return 2*ceil(r - 0.5)
    else:
        return 2*ceil(r) - 1

part1 = 1
for i in range(len(times)):
    part1 *= solve(int(times[i]),int(dists[i]))

print(f"part 1: {part1}")
print(f"part 2: {solve(int(''.join(times)), int(''.join(dists)))}")
