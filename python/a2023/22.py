#one of my favorite problems.
from common import get_problem_lines

def cube_range(cube):
    def s2(a,b):
        return (a,b) if a <= b else (b,a)
    xl, xr = s2(cube[0], cube[3])
    yl, yr = s2(cube[1], cube[4])
    zl, zr = s2(cube[2], cube[5])
    return [(x, y, z) for x in range(xl, xr+1) for y in range(yl, yr+1) \
            for z in range(zl, zr+1)]

cubes = list()
for line in get_problem_lines():
    (l, r) = line.split('~')
    cubes.append([int(c) for c in l.split(',') + r.split(',')])

# this also topologically sorts the graph later!!!
cubes.sort(key=lambda cube: cube[2])
occupied = set()
for cube in cubes:
    for loc in cube_range(cube):
        occupied.add(loc)

changed = True
while changed:
    changed = False
    for i in range(len(cubes)):
        if cubes[i][2] == 0 or cubes[i][5] == 0:
            continue
        for loc in cube_range(cubes[i]):
            occupied.remove(loc)
        cube_ = [cubes[i][0], cubes[i][1], cubes[i][2]-1, \
                cubes[i][3], cubes[i][4], cubes[i][5]-1]
        if all((loc not in occupied for loc in cube_range(cube_))):
            cubes[i] = cube_
            changed = True
        for loc in cube_range(cubes[i]):
            occupied.add(loc)

cubes = [(i, cube) for i, cube in enumerate(cubes)]

occupied = dict()
for i, cube in cubes:
    for loc in cube_range(cube):
        occupied[loc] = i

bwds = [set() for _ in cubes]
fwds = [set() for _ in cubes]
for i, cube in cubes:
    for x, y, z in cube_range(cube):
        z = z - 1
        j = occupied.get((x,y,z))
        if j is not None and j != i:
            bwds[i].add(j)
            fwds[j].add(i)

cubes = [i for i, _ in cubes]

part1 = sum(all(len(bwds[j]) != 1 for j in fwds[i]) for i in cubes)
print(f"part 1: {part1}")

# topologically sorted!
part2 = 0
for i in cubes:
    falls = {i}
    for j in cubes[i+1:]:
        if len(bwds[j]) == 0:
            continue
        if all((b in falls for b in bwds[j])):
            falls.add(j)
            part2 += 1

#print(k)
print(f"part 2: {part2}")
