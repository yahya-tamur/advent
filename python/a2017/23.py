from problem import gpl

inss = [line.split(' ') for line in gpl()]

def run(a, lastline=None):
    if lastline is None:
        lastline = len(inss)
    r = dict()

    for ins in inss:
        for reg in ins[1:]:
            if reg.isalpha():
                r[reg] = 0
            else:
                r[reg] = int(reg)
    r['a'] = a

    p1 = 0
    pc = 0
    while pc < lastline:
        ins, a, b = inss[pc]
        match ins:
            case 'set':
                r[a] = r[b]
            case 'sub':
                r[a] -= r[b]
            case 'mul':
                p1 += 1
                r[a] *= r[b]
            case 'jnz':
                if r[a] != 0:
                    pc += r[b]
                    continue
        pc += 1

    return(p1, r)

print(f"part 1: {run(0)[0]}")

# Looking at reddit, I think the only differences between users
# is the first line, set b <?>. This is a bit more general.

startreg, endreg = inss[0][1], inss[1][1]
incr = abs(int(inss[-2][2]))
_, r = run(1, 20)
start, end = r[startreg], r[endreg]

from math import ceil, sqrt
p2 = 0
for b in range(start, end + 1, incr):
    for d in range(2, ceil(sqrt(end))):
        if b % d == 0:
            p2 += 1
            break

print(f"part 2: {p2}")
