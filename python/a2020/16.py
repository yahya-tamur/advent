from common import gp

rules, yours, nearby = gp().split('\n\n')

rudi = dict()
p1rudi = set()
labels = list()
for rline in rules.split('\n'):
    label, _, nums = rline.partition(': ')
    a, b, _, c, d = nums.replace('-',' ').split(' ')
    a, b, c, d = int(a), int(b), int(c), int(d)
    rudi[label] = (a,b,c,d)
    p1rudi |= {(a,b),(c,d)}
    labels.append(label)

yours = yours[yours.find('\n')+1:]
yours = [int(i) for i in yours.split(',')]

nearby = [[int(i) for i in n.split(',')] for n in nearby.split('\n')[1:] if n]
nearby_ = list()

p1 = 0
for n in nearby:
    ok = True
    for x in n:
        if all((x not in range(u, v+1) for (u, v) in p1rudi)):
            p1 += x
            ok = False
    if ok:
        nearby_.append(n)
nearby = nearby_

print(f"part 1: {p1}")

options = {label: set() for label in labels}

for i in range(len(nearby[0])):
    for label in labels:
        a, b, c, d = rudi[label]
        ok = True
        if all([n[i] in range(a,b+1) or n[i] in range(c,d+1) for n in nearby]):
            options[label].add(i)

matches = dict()
while len(matches) < len(labels):
    (label, (opt,)) = next(( (label,opts) for label, opts in options.items() if len(opts) == 1 ))
    matches[label] = opt
    del options[label]
    for opts in options.values():
        opts.discard(opt)

p2 = 1
for label, i in matches.items():
    if 'departure' in label:
        p2 *= yours[i]


print(f"part 2: {p2}")
