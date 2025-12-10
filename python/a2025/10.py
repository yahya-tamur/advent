from problem import get_problem, get_problem_lines, look
from collections import deque

p1 = 0
for line in get_problem_lines():
    l, r = line.split('] ')
    r, _ = r.split(' {')
    start = sum((l[i+1] == '#') << i for i in range(len(l)-1))
    buttons = eval(r.replace(' ',',').replace(')',',)'))
    buttons = tuple(sum(1 << b for b in button) for button in buttons)

    seen  = set()
    queue = deque([(start, 0)])

    while queue:
        n, steps = queue.popleft()

        if n in seen:
            continue
        seen.add(n)

        if n == 0:
            p1 += steps
            break

        for b in buttons:
            queue.append((n ^ b, steps+1))
print(f"part 1: {p1}")

import numpy as np
from scipy.optimize import linprog

p2 = 0
for i, line in enumerate(get_problem_lines()):
    l, r = line.split(' {')
    _, l = l.split('] ')

    b = np.array(eval(r[:-1]))

    buttons = eval(l.replace(' ',',').replace(')',',)'))
    
    m = max(max(b) for b in buttons) + 1

    a = np.array([[int(i in b) for b in buttons] for i in range(m)])

    c = np.ones(len(buttons))


    p2 += sum(linprog(c, A_eq=a, b_eq=b, integrality=1).x)

print(f"part 2: {int(p2)}")
