from problem import gpl
from collections import defaultdict


m = defaultdict(int)

for line in gpl():
    a, b, c, d = line.find('@'), line.find(','), line.find(':'), line.find('x')

    x, y, dx, dy = int(line[a+1:b]), int(line[b+1:c]), int(line[c+1:d]), int(line[d+1:])

    for x_ in range(x, x + dx):
        for y_ in range(y, y + dy):
            m[(x_, y_)] += 1

print(f"part 1: {sum((x > 1 for x in m.values()))}")

for line in gpl():
    a, b, c, d = line.find('@'), line.find(','), line.find(':'), line.find('x')

    c, x, y, dx, dy = int(line[1:a]), int(line[a+1:b]), int(line[b+1:c]), int(line[c+1:d]), int(line[d+1:])

    if all((m[(x_,y_)] == 1 for x_ in range(x, x + dx) for y_ in range(y, y + dy))):
        print(f"part 2: {c}")
        #break
