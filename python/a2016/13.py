from problem import gp
from collections import deque

num = int(gp())

seen = set()
active = deque([(0, 1+1j)])
p2 = None

while active:
    steps, z = active.popleft()

    if steps > 50 and p2 is None:
        p2 = len(seen)

    if z in seen:
        continue
    seen.add(z)

    if z == 31+39j:
        print(f"part 1: {steps}")

    for z_ in [z+d for d in (1,-1,1j,-1j)]:
        x, y = int(z_.real), int(z_.imag)
        if x < 0 or y < 0:
            continue
        if (x*x + 3*x + 2*x*y + y + y*y + num).bit_count() % 2 == 0:
            active.append((steps+1, z_))

print(f"part 2: {p2}")
