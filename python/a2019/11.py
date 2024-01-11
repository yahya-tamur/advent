from intcode import interact, get_code

code = get_code()

map = set()
loc = 0
dir = -1

_, sendrecv = interact(code.copy())

all = set()

signal = 0
while (resp := sendrecv(signal)) is not None:
    if resp[0]:
        map.add(loc)
    else:
        map.discard(loc)
    all.add(loc)
    if resp[1]:
        dir *= -1j
    else:
        dir *= 1j
    loc += dir
    signal = loc in map

print(f"part 1: {len(all)}")


map = set()
loc = 0
dir = -1

_, sendrecv = interact(code)

signal = 1
while (resp := sendrecv(signal)) is not None:
    if resp[0]:
        map.add(loc)
    else:
        map.discard(loc)
    if resp[1]:
        dir *= -1j
    else:
        dir *= 1j
    loc += dir
    signal = loc in map

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
