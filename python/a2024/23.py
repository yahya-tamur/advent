from problem import get_problem, get_problem_lines, look
from collections import defaultdict

nods = set()
cons = defaultdict(set)
for line in get_problem_lines():
    a, b = line.split('-')
    if b > a:
        a, b = b, a
    cons[a].add(b)
    nods.add(a)
    nods.add(b)

nods = sorted(nods)

cons = defaultdict(list, {k: sorted(v) for k, v in cons.items()})

ans = 0
for n1 in nods:
    for j in range(len(cons[n1])):
        n2 = cons[n1][j]
        for i in range(j):
            n3 = cons[n1][i]
            if n3 in cons[n2]:
                if n1[0] == 't' or n2[0] == 't' or n3[0] == 't':
                    ans += 1
print(f"part 1: {ans}")

# largest connected subset of the set lst
def largest_connecteds(lst):
    if not lst:
        return [set()]
    m = 0
    ans = []
    for x in lst:
        sets = largest_connecteds(set(cons[x]) & lst)
        if len(sets[0]) + 1 < m:
            continue
        for s in sets:
            s.add(x)
        if len(sets[0]) > m:
            ans = sets
            m = len(sets[0])
        else:
            ans += sets
    return ans

print(f"part 2: {','.join(sorted(largest_connecteds(set(nods))[0]))}")
