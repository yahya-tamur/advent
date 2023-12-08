from common import get_problem
from collections import defaultdict

input = get_problem()

input = input.split('\n')

splits = dict()

for line in input[1:]:
    if not line.strip():
        continue
    (l,r) = line.split(' -> ')
    splits[(l[0],l[1])] = {(l[0], r), (r, l[1])}

start = list(input[0])

def ans(iterations):

    pairs = defaultdict(int)

    for i in range(len(start)-1):
        pairs[(start[i], start[i+1])] += 1

    for _ in range(iterations):
        pairs_ = defaultdict(int)
        for (t, n) in pairs.items():
            for t_ in splits[t]:
                pairs_[t_] += n
        pairs = pairs_

    incidences = defaultdict(int)
    for ((l, r), n) in pairs.items():
        incidences[l] += n

    # the last char stays the same.
    incidences[start[-1]] += 1

    l = list(incidences.values())
    l.sort()
    return l[-1] - l[0]

print(f"part 1: {ans(10)}")
print(f"part 2: {ans(40)}")
