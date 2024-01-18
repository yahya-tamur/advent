from problem import gpl
from collections import defaultdict

pl = gpl()

m = defaultdict(bool)
for (i, c) in enumerate(pl[0][pl[0].find(': ')+2:]):
    m[i] = c == '#'

prop = dict()
for p in pl[1:]:
    prop[tuple((x == '#' for x in p[:5]))] = p[9] == '#'

def score(m):
    return sum((i_ for i_, v in m.items() if v))

prevl = -100
for n in range(500):

    if n == 20:
        print(f"part 1: {score(m)}")

    l = min((i for i, v in m.items() if v)) - 3
    r = max((i for i, v in m.items() if v)) + 3

    m_ = defaultdict(bool)
    for i in range(l, r + 1):
        m_[i] = prop[(m[i-2],m[i-1],m[i],m[i+1],m[i+2])]

    dl = l - prevl
    left = [m[i] for i in range(l,r+1)]
    right = [m_[i] for i in range(l+dl,r+1+dl)]

    if left == right:
        print(f"part 2: {(50000000000-n)*sum(m.values())*dl + score(m)}")
        break

    m = m_
    prevl = l
