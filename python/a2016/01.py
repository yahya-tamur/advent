from problem import gpl

def man(z):
    return int(abs(z.real) + abs(z.imag))

loc, dr = 0, 1
seen = set()
p2 = None

for ins in gpl()[0].split(', '):
    dr *= {'R': 1j, 'L':-1j}[ins[0]]
    if p2 is None:
        for _ in range(int(ins[1:])):
            loc += dr
            if loc in seen and p2 is None:
                p2 = man(loc)
            seen.add(loc)
    else:
        loc += int(ins[1:])*dr

print(f"part 1: {man(loc)}")
print(f"part 2: {p2}")
