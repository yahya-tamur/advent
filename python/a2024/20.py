from problem import get_problem, get_problem_lines, look
from collections import defaultdict, deque
from time import time

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

path = [start, next(start+d for d in (1,-1,1j,-1j) if m[start+d] == '.')]
ended = False

while not ended:
    z = path[-1]
    ended = True
    for z_ in (z+1, z-1, z+1j, z-1j):
        if z_ != path[-2] and m[z_] == '.':
            path.append(z_)
            ended = False
            break


def man(z, z_):
    return int(abs(z.real - z_.real) + abs(z.imag - z_.imag))

ans1, ans2 = 0, 0

for i in range(len(path)):
    for j in range(i+2, len(path)):
        if j - i - (l := man(path[i], path[j])) < 100:
            continue
        ans1 += l <= 2
        ans2 += l <= 20

print(f"part 1: {ans1}")
print(f"part 2: {ans2}")
