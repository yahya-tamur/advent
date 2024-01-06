from problem import gpl
from collections import defaultdict
from random import shuffle

edges = set()

for line in gpl():
    a, bs = line.split(': ')
    for b in bs.split(' '):
        edges.add((a,b))
        edges.add((b,a))

edges = {(a,b) for a,b in edges if a < b}
nodes = {a for a, _ in edges} | {b for _, b in edges}

def karger():
    edg = [(a,b) for a,b in edges]
    nod = {a for a in nodes}
    shuffle(edg)
    size = {n : 1 for n in nod}
    aliases = {n : n for n in nod}

    def get_alias(n):
        m = aliases[n]
        if aliases[m] != m:
            while aliases[m] != m:
                m = aliases[m]
            aliases[n] = m
        return m

    while len(nod) > 2:
        (a, b) = edg.pop()
        a, b = get_alias(a), get_alias(b)
        if a == b:
            continue
        nod.remove(b)
        size[a] += size[b]
        aliases[b] = a
    true_edges = [(a, b) for (a, b) in edges if get_alias(a) != get_alias(b)]
    if len(true_edges) != 3:
        return None
    a, b = nod
    return size[get_alias(a)]*size[get_alias(b)]

ans = None
while ans is None:
    ans = karger()

print(f"part 1: {ans}")
