from problem import gpl

bots = [[] for _ in range(256)]
specs = [None for _ in range(256)]

for line in gpl():
    words = line.split(' ')
    if line[0] == 'b':
        b, l, h = (int(x) for x in (words[1], words[6], words[-1]))
        specs[b] = (l,h)
    else:
        v, b = (int(x) for x in (words[1], words[-1]))
        bots[b].append(v)

active = [i for i, b in enumerate(bots) if len(b) >= 2]

while active:
    bot = active.pop()
    a, b = bots[bot]
    bots[bot].clear()
    if a > b:
        a, b = b, a
    if (a,b) == (17, 61):
        print(f"part 1: {bot}")
    b1, b2 = specs[bot]
    bots[b1].append(a)
    bots[b2].append(b)
    for bi in (b1, b2):
        if len(bots[bi]) == 2:
            active.append(bi)

print(f"part 2: {bots[0][0] * bots[1][0] * bots[2][0]}")
