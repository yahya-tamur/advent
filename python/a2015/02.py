from problem import gpl

p1, p2 = 0, 0

for line in gpl():
    xyz = [int(c) for c in line.split('x')]
    xyz.sort()
    x, y, z = xyz

    p1 += 3*x*y + 2*(x*z + y*z)
    p2 += 2*(x+y) + x*y*z

print(f"part 1: {p1}")
print(f"part 2: {p2}")
