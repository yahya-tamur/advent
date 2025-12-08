from problem import get_problem, get_problem_lines, look

def e_sq(a, b):
    a1, a2, a3 = a
    b1, b2, b3 = b
    d1, d2, d3 = (b1- a1), (b2-a2), (b3-a3)
    return d1*d1 + d2*d2 + d3*d3

dots = [eval(line) for line in get_problem_lines()]

# 1000 x 1000 is ok actually

connections = [(e_sq(a, b), i, j) for (j, b) in enumerate(dots) for (i, a) in enumerate(dots[:j])]

connections.sort()


# group id dot i belogns to
groups = [i for i in range(len(dots))]
# dots belonging to group id i
cogroups = [[i] for i in range(len(dots))]

group_sizes = [1 for i in range(len(dots))]
full_groups = len(dots)

for _, i, j in connections:
    if j < i:
        i, j = j, i
    if (gi := groups[i]) != (gj := groups[j]):
        group_sizes[gi] += group_sizes[gj]
        group_sizes[gj] = 0
        cogroups[gi] += cogroups[gj]
        for k in cogroups[gj]:
            groups[k] = gi
        cogroups[gj].clear()
        full_groups -= 1
        if full_groups == 1:
            print(dots[i][0], dots[j][0])
            print(f"part 2: {dots[i][0]*dots[j][0]}")

#print(groups)
#print(cogroups)
#print(group_sizes)

group_sizes.sort()

