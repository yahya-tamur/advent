from problem import get_problem_lines
from collections import defaultdict

m = defaultdict(lambda:'.')

for i, line in enumerate(get_problem_lines()):
    for j, c in enumerate(line):
        m[i+1j*j] = c

k = list(m.keys())
ans = 0
for d in (1, -1, 1j, -1j, 1+1j, 1-1j, -1-1j, -1+1j):
    for s in k:
        ans += m[s] == 'X' and m[s+d] == 'M' and m[s+2*d] == 'A' and m[s+3*d] == 'S'

print(f"part 1: {ans}")


ans = 0
for s in k:
    ans +=  m[s] == 'A' and \
            ((m[s-1-1j] == 'M' and m[s+1+1j] == 'S') or (m[s-1-1j] == 'S' and m[s+1+1j] == 'M')) and \
            ((m[s-1+1j] == 'M' and m[s+1-1j] == 'S') or (m[s-1+1j] == 'S' and m[s+1-1j] == 'M'))

print(f"part 2: {ans}")
