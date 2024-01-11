# unusually awful variable names here.

costs = dict()
makes = dict()
maps = dict()

from problem import gpl

def get_vals(n):
    i = n.find(' ')
    return (int(n[:i]), n[i+1:])

for line in gpl():
    l, r = line.split(' => ')
    rval, rname = get_vals(r)
    maps[rname] = list()
    makes[rname] = rval
    for ll in l.split(', '):
        lval, lname = get_vals(ll)
        maps[rname].append(lname)
        costs[(rname, lname)] = lval

from collections import defaultdict

excess = defaultdict(int)

toaccount = defaultdict(int)
toaccount['FUEL'] = 1

p1 = 0
while toaccount:
    name, num = toaccount.popitem()
    if name == 'ORE':
        p1 += num
        continue
    to_make = num // makes[name]
    if num % makes[name] != 0:
        to_make += 1

    for req in maps[name]:
        needed = to_make*costs[(name, req)]
        if excess[req] > needed:
            excess[req] -= needed
        else:
            toaccount[req] += needed - excess[req]
            excess[req] = 0
    excess[name] += to_make*makes[name] - num


print(f"part 1: {p1}")

# initial idea was to first repeat the above process as many times as
# possible, but that wasn't efficient.

# 🌟🌟🌟
# I don't know I felt smart about it.
# As good as binary search but harder to understand :)


# Basic idea:
# you have a certain amount of materials left over.
# a 'naive' approach would be to try to make one more fuel, then one more
# fuel, ...

# Instead, try to make 2*64 fuel.
# If it's possible, do it doing the minimum number of conversions.
# Then, try 2*63 ...

# minimum conversions, because if A -> 2B, it's as good if not better to have
# one A than 2B.

# this just means trying to use the ingredients you have
# before making more.

# but that's why repeating the part1 process as many times as possible first
# fails.


excess = defaultdict(int)
excess['ORE'] = 1000000000000

n = 2 ** 64
fuel = 0
while n > 0:
    toaccount = defaultdict(int)
    toaccount['FUEL'] = n
    delta = defaultdict(int)

    success = True
    while toaccount:
        name, num = toaccount.popitem()
        if name == 'ORE':
            #since this means we're trying to craft more ORE instead of
            #using what we have
            success = False
            break
        to_make = num // makes[name]
        if num % makes[name] != 0:
            to_make += 1

        for req in maps[name]:
            needed = to_make*costs[(name, req)]
            if excess[req] - delta[req] > needed:
                delta[req] += needed
            else:
                toaccount[req] += needed - (excess[req] - delta[req])
                delta[req] = excess[req]
        delta[name] -= to_make*makes[name] - num
    if success:
        fuel += n
        for (i, v) in delta.items():
            excess[i] -= v
    n //= 2

print(f"part 2: {fuel}")
