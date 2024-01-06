from problem import gpl

locs = {'E': 1, 'S': -1j, 'W': -1, 'N': 1j}
dirs = {'L': 1j, 'R': -1j}

p1loc = 0
p1dir = 1

p2loc = 0
wyp = 10+1j

for l in gpl():
    instr, val = l[0], int(l[1:])
    if instr in locs:
        p1loc += locs[instr]*val
        wyp += locs[instr]*val
    elif instr in dirs:
        p1dir *= dirs[instr] ** (val // 90)
        wyp *= dirs[instr] ** (val // 90)
    else:
        p1loc += val*p1dir
        p2loc += val*wyp

print(f"part 1: {int(abs(p1loc.real) + abs(p1loc.imag))}")
print(f"part 2: {int(abs(p2loc.real) + abs(p2loc.imag))}")
