from problem import get_problem, get_problem_lines
from collections import Counter

inp = [int(x) for x in get_problem()[:-1].split(' ')]

def itr(l):
    l_ = []
    for x in l:
        if x == 0:
            l_.append(1)
        elif len(str(x)) % 2 == 0:
            sx = str(x)
            ll, rr = sx[:len(sx)//2], sx[len(sx)//2:] 
            l_.append(int(ll))
            l_.append(int(rr))
        else:
            l_.append(x*2024)
    return l_

l = inp.copy()
for _ in range(25):
    l = itr(l)
print(f"part 1: {len(l)}")



seen = dict()

def itrn(x, n):
    if (x, n) in seen:
        return seen[(x, n)]
    if n == 0:
        c = Counter()
        c[x] += 1
        return c
    c = itrn(x, n - 1)
    c_ = Counter()
    for k, v in c.items():
        for t in itr([k]):
            c_[t] += v
    seen[(x, n)] = c_
    return c_

print(f"part 2: {sum(sum(itrn(x, 75).values()) for x in inp)}")

# I think I could have just made l a counter and repeat the same algorithm,
# that would have been simpler.

