from problem import gpl

pairs = [tuple(int(x) for x in line.split('-')) for line in gpl()]

pairs.sort(key=(lambda p: p[1]))


pairs_ = list()

for a, b in pairs:

    while pairs_ and pairs_[-1][1] + 1 >= a:
        a = min(a, pairs_.pop()[0])

    pairs_.append((a, b))

pairs = pairs_

print(f"part 1: {pairs[0][1] + 1}")

p2 = pairs[0][0] + 4294967295 - pairs[-1][1] + \
        sum(pairs[i+1][0] - pairs[i][1] - 1 for i in range(len(pairs)-1))

print(f"part 2: {p2}")
