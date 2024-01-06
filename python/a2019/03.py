from problem import gpl

# when do two complex range intersect??

wires = list()

dirs = {'U': 1j, 'D': -1j, 'L': -1, 'R': 1}

for line in gpl():
    wires.append(dict())
    acc = 0
    steps = 0
    for phrase in line.split(','):
        for _ in range(int(phrase[1:])):
            acc += dirs[phrase[0]]
            steps += 1
            wires[-1][acc] = steps

print(f"part 1: {min((int(abs(z.real) + abs(z.imag)) for z in wires[0].keys() & wires[1].keys()))}")
print(f"part 2: {min((s+wires[1][z] for z, s in wires[0].items() if z in wires[1]))}")
