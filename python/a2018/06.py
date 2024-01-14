# Draw a rectangle around all the points.
# A point's area is infinite if and only if there's a point on the border
# whose closest point is that point.

from problem import gpl
#from collections import defaultdict

pts = [tuple((int(u) for u in line.split(', '))) for line in gpl()]

x0, x1 = min((x for x, _ in pts)) - 1, max((x for x, _ in pts)) + 1
y0, y1 = min((y for _, y in pts)) - 1, max((y for _, y in pts)) + 1

best = dict()

def best(x, y):
    (bp, dist) = None, x1 - x0 + y1 - y0
    for (px, py) in pts:
        if (pdist := abs(py - y) + abs(px - x)) == dist:
            bp = None
        elif pdist < dist:
            bp, dist = (px, py), pdist
    return bp

okpts = set(pts)

for x in range(x0, x1+1):
    okpts.discard(best(x, y0))
    okpts.discard(best(x, y1))

for y in range(y0, y1+1):
    okpts.discard(best(x0, y))
    okpts.discard(best(x1, y))

counts = {p: 0 for p in okpts}
for x in range(x0, x1+1):
    for y in range(y0, y1+1):
        if (b := best(x, y)) in okpts:
            counts[b] += 1

print(f"part 1: {max(counts.values())}")

# 🌟🌟🌟 if it works
# Unnecessary optimization,
# p1 is O(n^2 p) where p = number of points, n = edge length and it runs fine.
# This is O(p log p + n log n)

# Check if you need to expand search range. You can't use the method developed
# below since it forgets which points are border points.

hd = [sum((px - x0 for px, _ in pts))]
pts.sort(key=lambda p: p[0])
i = 0 # number of points whose x value is < x
for x in range(x0+1, x1+1):
    while i < len(pts) and pts[i][0] < x:
        i += 1
    hd.append(hd[-1] + 2*i - len(pts))

vd = [sum((py - y0 for _, py in pts))]
pts.sort(key=lambda p: p[1])
i = 0 # number of points whose y value is < y
for y in range(y0+1, y1+1):
    while i < len(pts) and pts[i][1] < y:
        i += 1
    vd.append(vd[-1] + 2*i - len(pts))

#works!
#def total_dist(x, y):
    #return hd[x-x0] + vd[y-y0]

#now we want to find number of pairs such that hd[x] + hd[y] < 10_000

hd.sort()
vd.sort()

def num_less_than(lst, n):
    l, r = 0, len(lst)
    while r - l > 0:
        m = (l + r) // 2
        if lst[m] >= n:
            r = m
        else:
            l = m + 1
    return l

print(f"part 2: {sum((num_less_than(vd, 10_000 - x) for x in hd))}")
