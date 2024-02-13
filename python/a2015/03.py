from problem import gp

dirs = {'>': 1, '<': -1, '^': 1j, 'v': -1j}
p = gp().strip()

loc, seen = 0, {0}

for c in p:
    loc += dirs[c]
    seen.add(loc)

print(f"part 1: {len(seen)}")

seen.clear()
loc1, loc2 = 0, 0

for i in range(0, len(p), 2):
    loc1 += dirs[p[i]]
    if i+1 < len(p):
        loc2 += dirs[p[i+1]]

    seen.add(loc1)
    seen.add(loc2)


print(f"part 2: {len(seen)}")
