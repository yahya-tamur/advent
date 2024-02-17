def add3(a, b):
    a0, a1, a2 = a
    b0, b1, b2 = b
    return (a0 + b0, a1 + b1, a2 + b2)

weapons = [(8, 4, 0), (10, 5, 0),  (25, 6, 0), (40, 7, 0), (74, 8, 0)]
armors =  [(13, 0, 1),  (31, 0, 2), (53, 0, 3), (75, 0, 4), (102, 0, 5), (0, 0, 0)]
rings =  [(25, 1, 0), (50, 2, 0), (100, 3, 0), (20, 0, 1), (40, 0, 2),  (80, 0, 3), (0, 0, 0)]

l = len(rings) - 1
for i in range(l):
    for j in range(i):
        rings.append(add3(rings[i], rings[j]))

from problem import gpl

b_hp, b_atk, b_arm = [int(line.split(' ')[-1]) for line in gpl()]
hp = 100

p1 = 999999999
p2 = 0
for w in weapons:
    for a in armors:
        for r in rings:
            cost, atk, arm = add3(add3(w, a), r)
            dam = max(1, atk - b_arm)
            rnds = (b_hp // dam) + int(b_hp % dam != 0)
            b_dam = max(1, b_atk - arm)
            b_rnds = (hp // b_dam) + int(hp % b_dam != 0)

            if rnds <= b_rnds:
                p1 = min(p1, cost)
            else:
                p2 = max(p2, cost)

print(f"part 1: {p1}")
print(f"part 2: {p2}")
