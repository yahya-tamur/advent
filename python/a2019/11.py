from intcode import interact
from problem import gp

code = [int(i) for i in gp().strip().split(',')]

map = set()
loc = 0
dir = -1

send, recv = interact(code.copy())

all = set()

send(0)
while (color := next(recv, None)) is not None:
    if color:
        map.add(loc)
    else:
        map.discard(loc)
    all.add(loc)
    if next(recv):
        dir *= -1j
    else:
        dir *= 1j
    loc += dir
    send(loc in map)

print(f"part 1: {len(all)}")


map = set()
loc = 0
dir = -1

send, recv = interact(code)

send(1)
while (color := next(recv, None)) is not None:
    if color:
        map.add(loc)
    else:
        map.discard(loc)
    if next(recv):
        dir *= -1j
    else:
        dir *= 1j
    loc += dir
    send(loc in map)

l, r = min((int(z.imag) for z in map)), max((int(z.imag) for z in map))
u, d = min((int(z.real) for z in map)), max((int(z.real) for z in map))

print('part 2:')
for i in range(u,d+1):
    for j in range(l,r+1):
        if i+1j*j in map:
            print('#',end='')
        else:
            print(' ',end='')
    print()
