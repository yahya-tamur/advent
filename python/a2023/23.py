from common import get_problem_lines
from time import time

key = {'.': 0, '^': -1, '>': 1j, 'v': 1, '<': -1j}
lines = get_problem_lines()
nn, mm = len(lines), len(lines[0])
map = {i + j*1j: key[lines[i][j]] \
       for i in range(nn) for j in range(mm) \
        if lines[i][j] != '#'}

paths = [({1j}, 1j)]
maxlen = 0
while paths:
    visited, last = paths.pop()
    dirs = [1, -1, 1j, -1j] if map[last] == 0 else [map[last]]
    nexts = [last + d for d in dirs if last + d not in visited \
            and last + d in map]
    if len(nexts) == 0:
        maxlen = max(maxlen, len(visited))
        continue
    for n in nexts[1:]:
        paths.append((visited | {n}, n))
    visited.add(nexts[0])
    paths.append((visited, nexts[0]))

print(f"part 1: {maxlen - 1}")

# collapses long sequences of edges
# wouldn't be accurate if longest path didn't end in a node with one edge.
nodes = {c for c in map}
edges = {c: set() for c in nodes}
for c in nodes:
    for d in [1, -1, 1j, -1j]:
        if c + d in map:
            edges[c].add((c+d, 1))
to_remove = set()
for c in nodes:
    if len(edges[c]) == 2:
        (a, n), (b, m) = edges[c]
        if b in [n for n, _ in edges[a]]:
            continue
        if a in [n for n, _ in edges[b]]:
            continue
        edges[a].remove((c,n))
        edges[b].remove((c,m))
        edges[a].add((b,n+m))
        edges[b].add((a,n+m))
        edges.pop(c)
        to_remove.add(c)
nodes = nodes - to_remove

paths = [({1j}, 0, 1j)]
maxlen = 0
while paths:
    visited, ln, last = paths.pop()
    if last == nn-1 + (mm-2)*1j:
        maxlen = max(maxlen, ln)
    for node, d_ln in edges[last]:
        if node not in visited:
            paths.append((visited | {node}, ln + d_ln, node))

print(f"part 2: {maxlen}")


