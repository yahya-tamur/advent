from problem import gp

d = {'n': 1, 's': -1, 'nw': -1j, 'sw': -1-1j, 'ne': 1+1j, 'se': 1j}

def dist(z):
    #want: -1j -> -1j+1, -1j-1 -> -1j, 1j -> 1j-1, 1j+1 -> 1j
    def slip(z):
        a, b = z.real, z.imag
        return a-b + b*1j

    def man(z):
        return abs(z.real) + abs(z.imag)

    return int(min(man(loc), man(slip(loc))))

loc = 0
p2 = 0

for s in gp().strip().split(','):
    loc += d[s]
    p2 = max(dist(loc), p2)

print(f"part 1: {dist(loc)}")
print(f"part 2: {p2}")


