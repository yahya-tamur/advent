from problem import gpl

nodes = list()

for line in gpl():
    x, y, z = eval(line[line.find('<')+1: line.find('>')])
    r = int(line[line.find('r=')+2:])
    nodes.append((r,x,y,z))

r, x, y, z = max(nodes)
print(f"part 1: {sum((abs(x-x_) + abs(y-y_) + abs(z-z_) <= r for _, x_, y_, z_ in nodes))}")

