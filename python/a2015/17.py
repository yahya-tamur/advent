from problem import gpl
from collections import Counter, defaultdict

inp = [int(line) for line in gpl()]

# This was faster than I expected! Of course it can be exponential with bad
# inputs (1, 2, 4, 8, ...) but the complexity is also bounded by sum(inp)*len(inp)
# which in this case is 417*20

states = Counter({0: 1})
for i in inp:
    states = states + Counter({l+i: r for l, r in states.items()})

print(f"part 1: {states[150]}")

# 🌟🌟🌟 
# complex is a convenient type for pairs of numbers you want to add!

states = Counter({0: 1})
for i in inp:
    states = states + Counter({l+i+1j: r for l, r in states.items()})

_, p2 = min((l.imag, r) for l, r in states.items() if l.real == 150)

print(f"part 2: {p2}")
