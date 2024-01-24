# 🌟🌟🌟 
# why have all my solutions been so awful this year?

from problem import gp
from collections import defaultdict, deque


doors = defaultdict(set) # set for 4 bit info???!!??
dir = {'N': 1, 'S': -1, 'W': 1j, 'E': -1j}

# unintuitive :(
# data structures = algorithms
activestack = [[[0]],[[0]]]

for c in gp().strip()[1:-1]:
    if (d := dir.get(c)) is not None:
        for a in activestack[-1][-1]:
            doors[a].add(d)
        activestack[-1][-1] = {a + d for a in activestack[-1][-1]}
    elif c == '(':
        activestack.append([activestack[-1][-1].copy()])
    elif c == '|':
        activestack[-1].append(activestack[-2][-1].copy())
    elif c == ')':
        a = set()
        for aa in activestack[-1]:
            a |= aa
        activestack.pop()
        activestack[-1][-1] = a

active = deque([(0,0)])
seen = set()

p1, p2 = 0, 0
while active:
    a, s = active.popleft()
    if a in seen:
        continue
    seen.add(a)
    p1 = s
    p2 += s >= 1000
    for d in doors[a]:
        active.append((a+d, s+1))

print(f"part 1: {p1}")
print(f"part 2: {p2}")
