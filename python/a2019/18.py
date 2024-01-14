# fun problem. heuristics.
# part 2 takes about 40 seconds on my laptop.

# This took me more time than any other problem this year except maybe 25.

from problem import gpl
from math import inf
from collections import defaultdict, deque
from time import time
import heapq

map = {i+j*1j: c for i, line in enumerate(gpl()) for j, c in enumerate(line) if c != '#'}
keylocs = dict()

for z, mz in map.items():
    if mz == '.':
        map[z] = -10
    elif mz == '@':
        map[z] = -1
        keylocs[-1] = z
    elif mz.islower():
        map[z] = ord(mz) - ord('a')
        keylocs[ord(mz) - ord('a')] = z
    elif mz.isupper():
        map[z] = ord(mz) - ord('A') + 26
        keylocs[ord(mz) - ord('A') + 26] = z
    else:
        print(f'what is this?: {mz}')

def get_edg(start):
    edg = dict()
    for i in range(start,52):
        edg[i] = dict()
        seen = set()
        vvv = deque([(keylocs[i], 0)])

        while vvv:
            curr, steps = vvv.popleft()

            if curr in seen or curr not in map:
                continue
            seen.add(curr)

            mv = map[curr]
            if mv in range(-1,52) and mv != i:
                if mv not in edg[i]:
                    edg[i][mv] = steps
                continue
            for d in [1, -1, 1j, -1j]:
                vvv.append((curr+d, steps+1))
    return edg

def p1():

    edg = get_edg(-1)

    # steps, current, keys (26 bit int)
    acc = [(0, -1, 0)]
    states = set()
    found = 0

    while acc:

        steps, curr, keys = heapq.heappop(acc)

        if (curr, keys) in states:
            continue
        states.add((curr, keys))

        if keys + 1 == (1 << 26):
            return steps

        for (dest, dsteps) in edg[curr].items():
            if dest >= 26:
                if 1 << (dest - 26) & keys:
                    heapq.heappush(acc, (steps + dsteps, dest, keys))
            elif dest >= 0:
                heapq.heappush(acc, (steps + dsteps, dest, keys | (1 << dest)))
            else:
                heapq.heappush(acc, (steps + dsteps, dest, keys))

print(f"part 1: {p1()}")

start = keylocs[-1]
for d in [0, 1, -1, 1j, -1j]:
    del map[start+d]

#robot starts: -5 through -2
for i, d in enumerate([1+1j, 1-1j, -1+1j, -1-1j]):
    map[start+d] = -2-i
    keylocs[-2-i] = start + d

robdone = [0, 0, 0, 0]
for z in range(26):
    vz = keylocs[z]
    if vz.real > start.real and vz.imag > start.imag:
        robdone[0] |= 1 << z
    if vz.real > start.real and vz.imag < start.imag:
        robdone[1] |= 1 << z
    if vz.real < start.real and vz.imag > start.imag:
        robdone[2] |= 1 << z
    if vz.real < start.real and vz.imag < start.imag:
        robdone[3] |= 1 << z

def p2():

    edg = get_edg(-5)

    # steps, current, keys (26 bit int)
    acc = [(0, (-2, -3, -4, -5), 0)]
    states = set()
    found = 0

    while acc:
        steps, curr, keys = heapq.heappop(acc)

        if (curr, keys) in states:
            continue

        states.add((curr, keys))

        if keys + 1 == (1 << 26):
            return steps

        for i in range(4):
            if (robdone[i] & keys) == robdone[i]:
                continue
            for (dest, dsteps) in edg[curr[i]].items():
                curr_ = list(curr)
                curr_[i] = dest
                curr_ = tuple(curr_)
                if dest >= 26:
                    if 1 << (dest - 26) & keys:
                        heapq.heappush(acc, (steps + dsteps, curr_, keys))
                elif dest >= 0:
                    heapq.heappush(acc, (steps + dsteps, curr_, keys | (1 << dest)))
                else:
                    heapq.heappush(acc, (steps + dsteps, curr_, keys))

print(f"part 2: {p2()}")
