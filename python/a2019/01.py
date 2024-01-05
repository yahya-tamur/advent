from common import gpl

f = lambda i: (i // 3) - 2

p1 = 0
p2 = 0
for l in gpl():
    p1 += f(int(l))
    d = f(int(l))
    while d > 0:
        p2 += d
        d = f(d)

print(f"part 1: {p1}")
print(f"part 2: {p2}")
