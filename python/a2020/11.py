from common import gpl

map = {i + j*1j for i, line in enumerate(gpl()) for j, c in enumerate(line) \
        if c == 'L'}

occupied, occupied_ = set(), set()

changed = True
while changed:
    changed = False
    for z in map:
        around = len([z + d for d in \
                [1,-1,1j,-1j,1+1j,1-1j,-1+1j,-1-1j] if z+d in occupied])
        if z not in occupied:
            if around == 0:
                occupied_.add(z)
                changed = True
            else:
                occupied_.discard(z)
        if z in occupied:
            if around >= 4:
                occupied_.discard(z)
                changed = True
            else:
                occupied_.add(z)
    occupied, occupied_ = occupied_, occupied

print(f"part 1: {len(occupied)}")
from math import sqrt

input = gpl()
n, m = len(input), len(input[0])
surrounding = {z: set() for z in map}
for z in map:
    for d in [1,-1,1j,-1j,1+1j,1-1j,-1+1j,-1-1j]:
        z_ = z + d
        while z_.real >= 0 and z_.imag >= 0 and z_.real < n and z_.imag < m:
            if z_ in map:
                surrounding[z].add(z_)
                break
            z_ += d

occupied, occupied_ = set(), set()

changed = True
while changed:
    changed = False
    for z in map:
        around = len(surrounding[z] & occupied)
        if z not in occupied:
            if around == 0:
                occupied_.add(z)
                changed = True
            else:
                occupied_.discard(z)
        if z in occupied:
            if around >= 5:
                occupied_.discard(z)
                changed = True
            else:
                occupied_.add(z)
    occupied, occupied_ = occupied_, occupied

print(f"part 2: {len(occupied)}")
