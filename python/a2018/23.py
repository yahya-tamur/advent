from problem import gpl

nodes = list()

for line in gpl():
    x, y, z = eval(line[line.find('<')+1: line.find('>')])
    r = int(line[line.find('r=')+2:])
    nodes.append((r,x,y,z))

r, x, y, z = max(nodes)

print(f"part 1: {sum((abs(x-x_) + abs(y-y_) + abs(z-z_) <= r for _, x_, y_, z_ in nodes))}")

_, xyz = max(( (sum((abs(x-x_) + abs(y-y_) + abs(z-z_) <= r_ for r_, x_, y_, z_ in nodes)), [x,y,z]) for _, x, y, z in nodes))

# Doesn't always get the right answer. Not sure about this problem -- the most
# convincing solutions I've seen use z3.

prev_xyz = "something else"
while prev_xyz != xyz:
    prev_xyz = xyz
    for i in range(3):

        scanline = list()
        for [r, *xyz_] in nodes:
            if (r_ := r - sum((abs(c - c_) for j, (c, c_) in enumerate(zip(xyz, xyz_)) if i != j ))) >= 0:
                scanline.append((xyz_[i] - r_, 1))
                scanline.append((xyz_[i] + r_ + 1, -1))

        scanline.sort()
        partial_sum, highest, best = 0, 0, 0
        for k, (_, d) in enumerate(scanline):
            partial_sum += d
            if partial_sum > highest:
                highest = partial_sum
                best = k
        if scanline:
            if scanline[best][0]*scanline[best+1][0] < 0:
                xyz[i] = 0
            elif abs(scanline[best][0]) < abs(scanline[best+1][0]):
                xyz[i] = scanline[best][0]
            else:
                xyz[i] = scanline[best+1][0]

print(f"part 2: {sum((abs(c) for c in xyz))}")
