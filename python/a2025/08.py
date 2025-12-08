from problem import get_problem, get_problem_lines, look
from heapq import nlargest

def e_sq(a, b):
    a1, a2, a3 = a
    b1, b2, b3 = b
    d1, d2, d3 = (b1- a1), (b2-a2), (b3-a3)
    return d1*d1 + d2*d2 + d3*d3

dots = [eval(line) for line in get_problem_lines()]

# 1000 x 1000 is ok actually

connections = [(i, j) for j in range(1000) for i in range(j)]
connections.sort(key=(lambda ij: e_sq(dots[ij[0]], dots[ij[1]])))

# group id dot i belogns to
groups = [i for i in range(len(dots))]
# dots belonging to group id i
cogroups = [[i] for i in range(len(dots))]

group_sizes = [1 for i in range(len(dots))]
full_groups = len(dots)

for n, (i, j) in enumerate(connections):
    if n == 1000:
        a, b, c = nlargest(3, group_sizes)
        print(f"part 1: {a*b*c}")
    if j < i:
        i, j = j, i
    # not fully optimized (wikipedia 'disjoint-set data structure')
    # but n=1000 here
    if (gi := groups[i]) != (gj := groups[j]):
        group_sizes[gi] += group_sizes[gj]
        group_sizes[gj] = 0
        cogroups[gi] += cogroups[gj]
        for k in cogroups[gj]:
            groups[k] = gi
        cogroups[gj].clear()
        full_groups -= 1
        if full_groups == 1:
            print(f"part 2: {dots[i][0]*dots[j][0]}")
            exit()
