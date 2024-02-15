from problem import gpl

names = dict()
half_hap = dict()

for line in gpl():
    words = line.split(' ')
    l, r = words[0], words[-1][:-1]

    for n in (l, r):
        if n not in names:
            names[n] = len(names)
    l, r = names[l], names[r]

    half_hap[(l, r)] = int(words[3]) * (1 if words[2] == 'gain' else -1)

hap = dict()
for i in range(len(names)):
    for j in range(i):
        hap[(i,j)] = half_hap[(i,j)] + half_hap[(j,i)]
        hap[(j,i)] = hap[(i,j)]

def search(hap, names):
    active = [(0, 0, 0)]
    ans = 0

    # This is straight up O(n!). Though n <= 9, so n! ~= 360,000.

    while active:
        steps, src, items = active.pop()

        if items == (1 << len(names)) - 1 and src == 0:
            ans = max(ans, steps)
            continue

        for dst in range(len(names)):
            if (1 << dst) & items or dst == src:
                continue
            active.append((steps + hap[(src, dst)], dst, (1 << dst) | items))
    return ans

print(f"part 1: {search(hap, names)}")

for i in range(len(names)):
    hap[(i, len(names))] = 0
    hap[(len(names), i)] = 0

names['me'] = len(names)

print(f"part 2: {search(hap, names)}")
