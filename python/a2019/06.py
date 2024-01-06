from problem import gpl
from collections import defaultdict

com = defaultdict(set)
for line in gpl():
    l, r = line.split(')')
    print(l,r)
    com[l].add(r)

def dfs(node, depth=0):
    return depth + sum((dfs(m,depth+1) for m in com[node]))

print(f"part 1: {dfs('COM')}")

for l, rs in com.items():
    for r in rs:
        com[r].add(l)

visited = set()
def find(node, target):
    if node in visited:
        return None
    visited.add(node)
    if node == target:
        return 0
    for m in com[node]:
        if (i := find(m, target)) is not None:
            return i + 1
    return None

print(f"part 2: {find('YOU','SAN')-2}")


