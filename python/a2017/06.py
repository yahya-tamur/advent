from problem import gp

inp = [int(x) for x in gp().strip().split('\t')]

seen = dict()

k = 0
while tuple(inp) not in seen:
    seen[tuple(inp)] = k
    k += 1

    i = 0
    for i_, x in enumerate(inp):
        if x > inp[i]:
            i = i_

    h = inp[i]
    inp[i] = 0
    for j in range(1,h+1):
        inp[(i+j) % len(inp)] += 1

print(f"part 1: {k}")
print(f"part 2: {k-seen[tuple(inp)]}")
