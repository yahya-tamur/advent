from problem import gp
from collections import deque
from md5 import fast_md5

inp = gp().strip()

dirs = {'U': -1, 'D': 1, 'L': -1j, 'R': 1j}

active = deque([(0, "")])
p1, p2 = "", ""

while active:
    loc, path = active.popleft()

    if loc == 3+3j:
        if p1 == "":
            p1 = path
        p2 = len(path)
        continue

    if int(loc.real) not in range(4) or int(loc.imag) not in range(4):
        continue

    h = fast_md5(inp + path)
    for d in ('UDLR'[i] for i, c in enumerate(h[:4]) if c in 'bcdef'):

        active.append((loc + dirs[d], path + d))

print(f"part 1: {p1}")
print(f"part 2: {p2}")
