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

def vw(node):
    weights = [(x, vw(x)) for x in mor[node]]
    weights = [(ww + wht[x], ww) for (x, ww) in weights]
    mlem = {w[0] for w in weights}
    if len(mlem) >= 2:
        weights.sort()
        required, met = (weights[0][0], weights[-1][1]) \
                if weights[1][0] == weights[0][0] else (weights[-1][0], weights[0][0])
        print(f"part 2: {required - met}")
        from sys import exit
        exit()
    return sum((w[0] for w in weights))

vw(one)
