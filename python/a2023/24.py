from problem import get_problem_lines

hailstones = list()
for line in get_problem_lines():
    line = line.replace(' @ ', ', ')
    hailstones.append([int(x) for x in line.split(', ')])

hailstones.sort()

#doesn't account for if h1 == h2
#a dx1 + x1 = b dx2 + x2
#a dy1 + y1 = b dy2 + y2

# [dx1 -dx2] [a] = [x2 - x1]
# [dy1 -dy2] [b]   [y2 - y1]

# ans = (a*dx1 + x1, a*dy1 + y1)

def solve2(m, v):
    (a, b), (c, d) = m
    invdet = 1/(a*d - b*c)
    x, y = v
    return invdet*(d*x - b*y), invdet*(-c*x + a*y)

def int_xy(h1, h2):
    x1, y1, _, dx1, dy1, _ = h1
    x2, y2, _, dx2, dy2, _ = h2

    if dy2*dx1 == dx2*dy1:
        return None

    m = [[dx1, -dx2], [dy1, -dy2]]
    v = [x2 - x1, y2 - y1]

    a, b = solve2(m, v)

    if a <= 0 or b <= 0:
        return None
    return (a*dx1 + x1, a*dy1 + y1)

part1 = 0
low, high = 200000000000000, 400000000000000
#low, high = 7, 27

for i, h1 in enumerate(hailstones):
    for j, h2 in enumerate(hailstones):
        if i == j:
            continue
        if (xy := int_xy(h1, h2)) is not None:
            x, y = xy
            if x >= low and x <= high and y >= low and y <= high:
                part1 += 1

print(f"part 1: {part1 // 2}")

m = list()
b = list()

for h1, h2 in zip(hailstones[:4], hailstones[1:5]):
    m.append([h1[4] - h2[4], h2[3] - h1[3], h2[1] - h1[1], h1[0] - h2[0]])
    b.append(h1[0]*h1[4] - h2[0]*h2[4] + h2[1]*h2[3] - h1[1]*h1[3])

from scipy.linalg import solve
_, _, dr1, dr2 = solve(m, b)

m = list()
b = list()
for h1, h2 in zip(hailstones[:4], hailstones[1:5]):
    m.append([h1[5] - h2[5], h2[3] - h1[3], h2[2] - h1[2], h1[0] - h2[0]])
    b.append(h1[0]*h1[5] - h2[0]*h2[5] + h2[2]*h2[3] - h1[2]*h1[3])

_, _, _, dr3 = solve(m, b)

#positions aren't numerically accurate but velocities are.
dr1, dr2, dr3 = round(dr1), round(dr2), round(dr3)

from decimal import *

getcontext().prec = 1000

h1, h2 = hailstones[:2]
m = [[Decimal(h1[4] - dr2), Decimal(dr1 - h1[3])], \
     [Decimal(h2[4] - dr2), Decimal(dr1 - h2[3])]]

v = [Decimal(h1[0]*(h1[4] - dr2) + h1[1]*(dr1 - h1[3])), \
    Decimal(h2[0]*(h2[4] - dr2) + h2[1]*(dr1 - h2[3]))]

x, y = solve2(m, v)

m = [[Decimal(h1[5] - dr3), Decimal(dr1 - h1[3])], \
     [Decimal(h2[5] - dr3), Decimal(dr1 - h2[3])]]

v = [Decimal(h1[0]*(h1[5] - dr3) + h1[2]*(dr1 - h1[3])), \
    Decimal(h2[0]*(h2[5] - dr3) + h2[2]*(dr1 - h2[3]))]

_, z = solve2(m, v)

print(f"part 2: {round(x) + round(y) + round(z)}")


