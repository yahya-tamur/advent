from problem import gpl
import sys

x, y, dx, dy = [], [], [], []

for line in gpl():
    x.append(int(line[10:16]))
    y.append(int(line[18:24]))
    dx.append(int(line[-7:-5]))
    dy.append(int(line[-3:-1]))

n = len(x)

message_height = 20

_, miny = min((y_, i) for i, y_ in enumerate(y))
_, maxy = max((y_, i) for i, y_ in enumerate(y))

minskip = ((y[maxy] - y[miny] + message_height) // (dy[miny] - dy[maxy])) - 300
map = [x[i] + minskip*dx[i] + 1j*(y[i] + minskip*dy[i]) for i in range(n)]

for skip in range(minskip, minskip + 300):
    x0, x1 = int(min((z.real for z in map))), int(max((z.real for z in map)))
    y0, y1 = int(min((z.imag for z in map))), int(max((z.imag for z in map)))
    #print(skip, x1 - x0, y1 - y0, file=sys.stderr)
    if x1 - x0 < 150 and y1 - y0 < 500:
        mmm = set(map)
        found = False
        for j in range(y0, y1+1):
            for i in range(x0, x1+1):
                z = i+1j*j
                # Might need to adjust this for different inputs.
                if all((z + 1j*k in mmm for k in range(7))):
                    found = True
                if found:
                    break
            if found:
                break

        if found:
            print("part 1:")
            for j in range(y0, y1+1):
                for i in range(x0, x1+1):
                    if i+1j*j in mmm:
                        print('#', end='')
                    else:
                        print(' ', end='')
                print()
            print(f"part 2: {skip}")
    for i in range(n):
        map[i] += dx[i]+1j*dy[i]


