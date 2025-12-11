from problem import get_problem, get_problem_lines, look
from collections import defaultdict
import numpy as np

gates = defaultdict(list)

labels = set()
for line in get_problem_lines():
    l, r = line.split(': ')
    labels.add(l)
    for rr in r.split(' '):
        labels.add(rr)

ix = {l : i for i, l in enumerate(labels)}

# make adjecency matrix
a = np.zeros((len(labels), len(labels)))

for line in get_problem_lines():
    l, r = line.split(': ')
    for rr in r.split(' '):
        a[ix[l]][ix[rr]] += 1

# make path matrix
acc = a.copy()
paths = a.copy()

while acc.any():
    acc = acc @ a
    paths += acc

# just to make final expression more compact
from math import prod

p = lambda a,b: int(paths[ix[a]][ix[b]])
pp = lambda l:prod(p(l[i],l[i+1]) for i in range(len(l)-1))

print(f"part 1: {p('you','out')}")
print(f"part 2: {pp(('svr','dac','fft','out'))+pp(('svr','fft','dac','out'))}")
