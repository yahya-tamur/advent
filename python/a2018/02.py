from problem import gpl
from collections import defaultdict

def nmm(s, n):
    d = defaultdict(int)
    for c in s:
        d[c] += 1

    return n in d.values()

print(f"part 1: {sum((nmm(line, 2) for line in gpl()))*sum((nmm(line, 3) for line in gpl()))}")

pl = gpl()
for i, s1 in enumerate(pl):
    for s2 in pl[:i]:
        if sum((c1 != c2 for c1, c2 in zip(s1, s2))) == 1:
            print(f"part 2: {''.join((c1 for c1, c2 in zip(s1, s2) if c1 == c2))}")
            from sys import exit
            exit()

