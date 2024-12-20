from problem import get_problem, get_problem_lines, look
from collections import defaultdict, deque

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

start_ = next(start+d for d in (1, -1, 1j, -1j) if m[start+d] == '.')
path = [start, start_]

ended = False

while not ended:
    ended = True
    for d in (1, -1, 1j, -1j):
        nxt = path[-1] + d
        if nxt != path[-2] and m[nxt] == '.':
            path.append(nxt)
            ended = False
            break

def man(z, z_):
    return int(abs(z.real - z_.real) + abs(z.imag - z_.imag))

cheats1 = [0 for _ in range(len(m))]
cheats2 = [0 for _ in range(len(m))]

for i in range(len(path)):
    for j in range(i+2, len(path)):
        if (m := man(path[i], path[j])) <= 2:
            cheats1[j - i - m] += 1
        if (m := man(path[i], path[j])) <= 20:
            cheats2[j - i - m] += 1

print(f"part 1: {sum(cheats1[100:])}")
print(f"part 2: {sum(cheats2[100:])}")
