from problem import get_problem, get_problem_lines
from collections import defaultdict

m = defaultdict(lambda:100)
starts = []

for i, line in enumerate(get_problem_lines()):
    for j, c in enumerate(line):
        if c == '0':
            starts.append(i+1j*j)
        m[i+1j*j] = int(c)

ans = 0
ans2 = 0
for z in starts:
    reachable = set()
    stack = [z]
    while stack:
        loc = stack.pop()
        if m[loc] == 9:
            ans2 += 1
            reachable.add(loc)
        for loc_ in (loc+1, loc-1, loc+1j, loc-1j):
            if m[loc_] - m[loc] == 1:
                stack.append(loc_)
    ans += len(reachable)



print(f"part 1: {ans}")
print(f"part 2: {ans2}")
