from problem import gpl
from math import gcd

lines = gpl()
#backward!
asts = set(( (j,i) for i, line in enumerate(lines) for j, c in enumerate(line) \
        if c == '#' ))

p1 = (0,(-1,-1))
# a bit inefficient -- what we know about one asteroid should help with others.
for x, y in asts:
    ans = 0
    vv = set()
    for x_, y_ in asts:
        i, j = x - x_, y - y_
        if i == 0 and j == 0:
            continue
        vv.add((i // gcd(i,j), j // gcd(i,j)))
        if gcd(i,j) != 1:
            continue
    p1 = max(p1,(len(vv),(x,y)))

print(f"part 1: {p1[0]}")

pi, pj = p1[1]

from math import atan2
from collections import defaultdict

angdict = defaultdict(list)
for ast in asts:
    ai, aj = ast
    angdict[-atan2(ai-pi,aj-pj)].append((ai,aj))

anglist = list(angdict.items())
anglist.sort()

for _angle, group in anglist:
    group.sort(key=lambda ast:(ast[0]-pi)*(ast[0]-pi) + (ast[1]-pj)*(ast[1]-pj))

ind = 0
i = 0
while True:
    for _, group in anglist:
        if ind < len(group):
            i += 1
            if i == 200:
                print(f"part 2: {100*group[ind][0] + group[ind][1]}")
                from sys import exit
                exit()
    ind += 1
