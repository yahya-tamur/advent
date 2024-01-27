# I really, really should just make or find a union-find data structure.
from problem import gpl

cstls = list()

for line in gpl():
    xyzw = tuple([int(c) for c in line.split(',')])

    matches = list()
    for i, cstl in enumerate(cstls):
        for xyzw_ in cstl:
            if sum((abs(c - c_) for c, c_ in zip(xyzw, xyzw_))) <= 3:
                matches.append(i)
                break
    if len(matches) == 0:
        cstls.append({xyzw})
    else:
        cstls[matches[0]] |= {xyzw}
        for i in matches[-1:0:-1]:
            cstls[matches[0]] |= cstls[i]
            cstls.pop(i)

print(f"part 1: {len(cstls)}")
print(f"part 2: {0}")

