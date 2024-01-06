#BOUNDARIES:
# 4..5
# infer cubes:
# [-inf,4], [4,5], [6,inf]
# if you then see [9,10] create:

# OK JUST DO WHAT YOU'RE ACTUALLY SUPPOSED TO DO.

# cubes = <six nums>
from problem import get_problem_lines

# returns list of cubes.
def delete_cube(a, b):
    if a[0] > b[1] or a[1] < b[0] or a[2] > b[3] or a[3] < b[2] \
            or a[4] > b[5] or a[5] < b[4]:
        return [a]
    ans = list()
    for n in range(3):
        if a[2*n] < b[2*n] and b[2*n] <= a[2*n+1]:
            ans.append(a.copy())
            ans[-1][2*n+1] = b[2*n] - 1
            a[2*n] = b[2*n]
        if a[2*n] <= b[2*n+1] and b[2*n+1] < a[2*n+1]:
            ans.append(a.copy())
            ans[-1][2*n] = b[2*n+1]+1
            a[2*n+1] = b[2*n+1]
    return ans

cubes = list()

def total_vol(cs):
    return sum((x2-x1+1)*(y2-y1+1)*(z2-z1+1) for \
            (x1, x2, y1, y2, z1, z2) in cs)

part1done = False

s = get_problem_lines()
for line in s:
    line = line.replace(" x=","|").replace("..","|").replace(",y=","|").replace(",z=","|")
    if (not part1done) and len(line) > 30:
        print(f"part 1: {total_vol(cubes)}")
        part1done = True
    newcube = [int(x) for x in line.split("|")[1:]]
    cubes_ = list()
    for cube in cubes:
        cubes_.extend(delete_cube(cube, newcube))
    if line[1] == 'n':
        cubes_.append(newcube)
    cubes = cubes_
print(f"part 2: {total_vol(cubes)}")
