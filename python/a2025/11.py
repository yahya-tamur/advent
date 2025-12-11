from problem import get_problem, get_problem_lines, look
from collections import defaultdict
import numpy as np

gates = defaultdict(list)

for line in get_problem_lines():
    l, r = line.split(': ')
    for rr in r.split(' '):
        gates[l].append(rr)

labels = set(gates)
for r in gates.values():
    labels |= set(r)

labels = list(labels)
colabels = {l : i for i, l in enumerate(labels)}

a = np.zeros((len(labels), len(labels)))

for l in gates:
    for r in gates[l]:
        a[colabels[l]][colabels[r]] = 1

acc = a.copy()
paths = a.copy()

i = 0
while acc.any():
    print(i)
    acc = acc @ a
    paths += acc
    i += 1

cl = colabels

p2 = paths[cl['svr']][cl['dac']]*paths[cl['dac'],cl['fft']]*paths[cl['fft'],cl['out']] + \
        paths[cl['svr'], cl['fft']]*paths[cl['fft'],cl['dac']]*paths[cl['dac'],cl['out']]
print(f"part 2: {int(p2)}")
