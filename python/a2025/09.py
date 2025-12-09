from problem import get_problem, get_problem_lines, look

points = [eval(line) for line in get_problem_lines()]

def r(n):
    return n % len(points)

p1 = 0

for j in range(len(points)):
    for i in range(j):
        x1, y1 = points[i]
        x2, y2 = points[j]
        p1 = max(p1,(abs(x2 - x1)+1)*(abs(y2 - y1)+1))

print(f"part 1: {p1}")

# shrink
xs = [(p[0], i) for i, p in enumerate(points)]
xs.sort()

ys = [(p[1], i) for i, p in enumerate(points)]
ys.sort()

points_ = [0 for _ in range(len(points))]

x = 0
y = 0
for i in range(1, len(points)):
    x += 2*(xs[i][0] != xs[i-1][0])
    points_[xs[i][1]] += x
    y += 2j*(ys[i][0] != ys[i-1][0])
    points_[ys[i][1]] += y

# draw border
area = set()
for i in range(-1, len(points)-1):
    d = points_[i+1] - points_[i]
    d = d / abs(d)

    z = points_[i]
    while z != points_[i+1]:
        area.add(z)
        z += d

# dfs to color in
start = max((z.real, z.imag) for z in points_)
stack = [start[0]+start[1]*1j - 1 - 1j]

while stack:
    z = stack.pop()
    area.add(z)
    for d in (1,-1,1j,-1j):
        if z+d not in area:
            stack.append(z+d)

area = {(int(z.real)//2, int(z.imag)//2) for z in area}
points_ = [(int(z.real)//2, int(z.imag)//2) for z in points_]

# brute force
p2 = 0
for j in range(len(points_)):
    for i in range(j):
        x0, x1 = sorted((points_[i][0], points_[j][0]))
        y0, y1 = sorted((points_[i][1], points_[j][1]))
        if all(((x, y) in area for x in range(x0, x1+1) for y in range(y0, y1+1))):
            p2 = max(p2, (1+abs(points[i][0] - points[j][0]))*(1+abs(points[i][1] - points[j][1])))

print(f"part 2: {p2}")
