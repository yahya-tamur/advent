from problem import get_problem, get_problem_lines, look
from heapq import nlargest
from time import time

AAA = time()
def e_sq(a, b):
    a1, a2, a3 = a
    b1, b2, b3 = b
    d1, d2, d3 = (b1- a1), (b2-a2), (b3-a3)
    return d1*d1 + d2*d2 + d3*d3

dots = [eval(line) for line in get_problem_lines()]

# 1000 x 1000 is ok actually

connections = [(i, j) for j in range(len(dots)) for i in range(j)]
connections.sort(key=(lambda ij: e_sq(dots[ij[0]], dots[ij[1]])))


# group id dot i belogns to
groups = list(range(len(dots)))
sizes = [1 for _ in range(len(dots))]
full_groups = len(dots)

def find(i):
    while groups[i] != i:
        groups[i] = groups[groups[i]]
        i = groups[i]
    return i


def union(i, j):
    i, j = find(i), find(j)
    if i == j:
        return False
    if sizes[i] < sizes[j]:
        i, j = j, i
    groups[j] = i
    sizes[i] += sizes[j]
    sizes[j] = 0
    return True


for n, (i, j) in enumerate(connections):
    if n == 1000:
        a, b, c = nlargest(3, sizes)
        print(f"part 1: {a*b*c}")
    gi, gj = groups[i], groups[j]
    if union(gi,gj):
        full_groups -= 1
        if full_groups == 1:
            print(f"part 2: {dots[i][0]*dots[j][0]}")
            print(time() - AAA)
            break
