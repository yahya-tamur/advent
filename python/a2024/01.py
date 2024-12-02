l, r = [], []

from problem import get_problem_lines

for line in get_problem_lines():
    lx, rx = line.split('   ')
    l.append(int(lx))
    r.append(int(rx))

l.sort()
r.sort()

print(f"part 1: {sum(abs(x - y) for x, y in zip(l, r))}")

from collections import defaultdict

r_ = defaultdict(int)
for x in r:
    r_[x] += 1

r = r_

print(f"part 2: {sum(x*r[x] for x in l)}")
