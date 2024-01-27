# 🌟🌟🌟
# This was a lot of fun! I'm really happy with how it turned out.
# The parse and the run functions are merged so I don't have to copy 'units'.
# (And the input file is pretty small)
# Parsing by removing the extra parts was a good idea, and so was defining
# constants so 'unit's feel like structs without any additional complexity.
# Though why not just define a struct at this point?

from problem import gpl
from collections import defaultdict

def run(boost):
    side = -1

    units = list()

    # I've just been really enjoying not looking at the regular expression
    # documentation recently. I know I should use it!
    for key, line in enumerate(gpl()):
        if ':' in line:
            side += 1
            continue
        if 'units' not in line:
            continue

        num, hp, *_, dam, damtyp, init = line \
                .replace('units each with ', '') \
                .replace('damage at initiative ', '') \
                .split(' ')

        num, hp, dam, init = int(num), int(hp), int(dam), int(init)

        res = defaultdict(lambda:1)
        if '(' in line:
            for sec in line[line.find('(')+1:line.find(')')].split('; '):
                coef = {'weak': 2, 'immune': 0}[sec[:sec.find(' ')]]
                for typ in sec[sec.find('to ')+3:].split(', '):
                    res[typ] = coef

        units.append([key, side, num, hp, res, dam, damtyp, init])

    key, side, num, hp, res, dam, damtyp, init = range(8)

    for u in units:
        if u[side] == 0:
            u[dam] += boost

    while len({u[side] for u in units}) == 2:
        targets = dict()
        units.sort(key=lambda u:(-u[num]*u[dam], -u[init]))
        for u in units:
            available = [ u_ for u_ in units if \
                    u_[side] != u[side] and u_[key] not in targets.values()]
            if not available:
                continue
            trt = max(available, key=lambda u_: \
                    (u_[res][u[damtyp]]*u[num]*u[dam], u_[num]*u_[dam], u_[init]))
            if trt[res][u[damtyp]]*u[num]*u[dam] != 0:
                targets[u[key]] = trt[key]
        if len(targets) == 0:
            return (-1, -1)

        units.sort(key=lambda u:-u[init])
        for u in units:
            if u[num] <= 0 or u[key] not in targets:
                continue
            i = next((i for i, u_ in enumerate(units) if u_[key] == targets[u[key]]))
            units[i][num] -= u[num]*u[dam]*units[i][res][u[damtyp]] // units[i][hp]

        units = [u for u in units if u[num] > 0]
    return (units[0][side], sum((u[num] for u in units)))

print(f"part 1: {run(0)[1]}")

# Yes, I didn't look up how to do a binary search. How can you tell?
step, boost = 1 << 32, 1 << 32

while step > 0:
    if run(boost-step)[0] == 0:
        boost -= step
    step >>= 1

print(f"part 2: {run(boost)[1]}")
