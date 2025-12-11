from problem import get_problem, get_problem_lines, look
import numpy as np
from scipy.sparse import coo_array
from collections import defaultdict
from time import time

ix = defaultdict(lambda:len(ix))

# make adjecency matrix
row, col, data = [], [], []

for line in get_problem_lines():
    l, rr = line.split(': ')
    for r in rr.split(' '):
        row.append(ix[l])
        col.append(ix[r])
        data.append(1)

a = coo_array((data, (row, col)), shape=(len(ix), len(ix)))

# make path matrix
a_2_n = a.copy()
paths = a.copy()

while a_2_n.sum():
    paths += a_2_n @ paths
    a_2_n = a_2_n @ a_2_n

# just to make final expression more compact
from math import prod

p = lambda a,b: int(paths[ix[a], ix[b]])
pp = lambda l:prod(p(l[i],l[i+1]) for i in range(len(l)-1))

print(f"part 1: {p('you','out')}")
print(f"part 2: {pp(('svr','dac','fft','out'))+pp(('svr','fft','dac','out'))}")
