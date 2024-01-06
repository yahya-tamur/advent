from problem import gp
from collections import deque

p1, p2 = [deque([int(i) for i in lines.split('\n')[1:]]) \
        for lines in gp().strip().split('\n\n')]
i=1

def score(p):
    return sum(( (len(p)-i)*p[i] for i in range(len(p)) ))

def combat(p1, p2):
    p1, p2 = p1.copy(), p2.copy()
    while len(p1) != 0 and len(p2) != 0:
        a, b = p1.popleft(), p2.popleft()
        if a > b:
            p1.append(a)
            p1.append(b)
        else:
            p2.append(b)
            p2.append(a)
    return score(max(p1, p2))

# return i, hand
def r_combat(p1, p2):
    p1, p2 = p1.copy(), p2.copy()
    mem = set()
    while len(p1) != 0 and len(p2) != 0:
        m = (tuple(p1), tuple(p2))
        if m in mem:
            return 1, score(p1)
        else:
            mem.add(m)
        a, b = p1.popleft(), p2.popleft()
        if len(p1) >= a and len(p2) >= b:
            if r_combat(deque(list(p1)[:a]), deque(list(p2)[:b]))[0] == 1:
                p1.append(a)
                p1.append(b)
            else:
                p2.append(b)
                p2.append(a)
        else:
            if a > b:
                p1.append(a)
                p1.append(b)
            else:
                p2.append(b)
                p2.append(a)
    if len(p1) == 0:
        return 2, score(p2)
    else:
        return 1, score(p1)


print(f"part 1: {combat(p1, p2)}")
print(f"part 2: {r_combat(p1, p2)[1]}")
