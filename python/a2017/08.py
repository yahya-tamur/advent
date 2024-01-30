from problem import gpl
from collections import defaultdict

wars = defaultdict(int)
p2 = 0
for line in gpl():
    x0, incdec, val, _, x1, cond, val2 = line.split(' ')
    val, val2 = int(val), int(val2)

    if incdec == 'dec':
        val = -val

    if eval(f"wars['{x1}'] {cond} {val2}"):
        wars[x0] += val
        p2 = max(p2, wars[x0])


print(f"part 1: {max(wars.values())}")
print(f"part 2: {p2}")
