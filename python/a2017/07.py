from problem import gp, gpl
from collections import defaultdict

wht = dict()

mor = dict()
comor = dict()

for line in gpl():
    l = line[:line.find(' ')]

    wht[l] = int(line[line.find('(')+1: line.find(')')])

    mor[l] = set()
    if '>' in line:
        for r in line[line.find('> ')+2:].split(', '):
            mor[l].add(r)
            comor[r] = l

one = next(iter(wht))

while one in comor:
    one = comor[one]

print(f"part 1: {one}")
