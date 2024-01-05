from common import gpl

input = list()
for line in gpl():
    input.append(( \
        line[:line.find(' (')].split(' '), \
        line[line.find(' (')+len(" (contains "):-1].split(', ')))

ingredients = set()
contains = dict()
for (lhs, rhs) in input:
    ingredients |= set(lhs)
    for r in rhs:
        contains[r] = set(lhs)

for (lhs, rhs) in input:
    for r in rhs:
        contains[r] &= set(lhs)

nonallergs = {i for i in ingredients if not any((i in v for v in contains.values()))}

p1 = 0
for (lhs, rhs) in input:
    p1 += len(set(lhs) & nonallergs)
print(f"part 1: {p1}")

determined = list()
while contains:
    for k in contains:
        if len(contains[k]) == 1:
            v = contains[k].pop()
            determined.append((k, v))
            for vs in contains.values():
                vs.discard(v)
            del contains[k]
            break

determined.sort()
p2 = ','.join((v for k, v in determined))

print(f"part 2: {p2}")
