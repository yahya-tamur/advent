from problem import get_problem_lines
from collections import defaultdict

ants = defaultdict(list)
alll = set()
allowed = set()

for i, line in enumerate(get_problem_lines()):
    for j, c in enumerate(line):
        allowed.add(i+1j*j)
        if c != '.':
            ants[c].append(i+1j*j)
            alll.add(i+1j*j)


def solve(part):
    ats = set()

    for antens in ants.values():
        for z in antens:
            for z_ in antens:
                if z == z_:
                    continue
                k = z + 2*(z_-z)
                while k in allowed:
                    ats.add(k)
                    k += z_ - z
                    if part == 1:
                        break
    if part == 1:
        return len(ats)
    return len(ats | alll)

print(f"part 1: {solve(1)}")
print(f"part 2: {solve(2)}")

