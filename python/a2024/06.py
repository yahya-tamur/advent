from problem import get_problem_lines
from collections import defaultdict

m = defaultdict(lambda:' ')
for i, line in enumerate(get_problem_lines()):
    for j, c in enumerate(line):
        m[i+1j*j] = c
cur = next(k for k, v in m.items() if v == '^')

def solve(m, cur):
    d = -1
    seen = {(cur, d)}

    while cur in m:
        while m[cur + d] == '#':
            d *= -1j
        cur += d
        if m[cur] == ' ':
            return {cur for cur, _ in seen}
        if (cur, d) in seen:
            return -1
        else:
            seen.add((cur, d))

first = solve(m, cur)
print(f"part 1: {len(first)}")

ans2 = 0

for k in first:
    if m[k] != '.':
        continue
    m[k] = '#'
    ans2 += solve(m, cur) == -1
    m[k] = '.'

print(f"part 2: {ans2}")
