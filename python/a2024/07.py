from problem import get_problem, get_problem_lines
from itertools import product

ans = 0

for line in get_problem_lines():
    l, r = line.split(': ')
    l = int(l)
    r = [int(x) for x in r.split(' ')]
    for ops in product(*[(0,1)]*(len(r) - 1)):
        t = r[0]
        for op, i in zip(ops, r[1:]):
            if op == 0:
                t += i
            else:
                t *= i

        if t == l:
            ans += l
            break

print(f"part 1: {ans}")





ans = 0

for line in get_problem_lines():
    l, r = line.split(': ')
    l = int(l)
    r = [int(x) for x in r.split(' ')]
    for ops in product(*[(0,1,2)]*(len(r) - 1)):
        t = r[0]
        for op, i in zip(ops, r[1:]):
            if op == 0:
                t += i
            elif op == 1:
                t *= i
            else:
                t = int(str(t) + str(i))

        if t == l:
            ans += l
            break

print(f"part 2: {ans}")
