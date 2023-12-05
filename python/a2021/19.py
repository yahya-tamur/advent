from common import get_problem_lines

vx = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

def dx(a,b):
    return (a[0]*b[0] + a[1]*b[1] + a[2]*b[2])

def cx(a,b):
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])

rots = [(v1, v2, cx(v1, v2)) for v1 in vx for v2 in vx if dx(v1,v2) == 0 ]

def rotate(v, rot):
    # v[0]*rot[0] + v[1]*rot[1] + v[2]*rot[2]
    return (v[0]*rot[0][0] + v[1]*rot[1][0] + v[2]*rot[2][0], \
            v[0]*rot[0][1] + v[1]*rot[1][1] + v[2]*rot[2][1], \
            v[0]*rot[0][2] + v[1]*rot[1][2] + v[2]*rot[2][2] )

def rotlist(vl, rot):
    return [rotate(v,rot) for v in vl]

scanners = list()

for line in get_problem_lines(2021,19):
    if line.find('scanner') != -1:
        scanners.append([])
    if line.find(',') != -1:
        (a,b,c) = line.split(',')
        scanners[-1].append((int(a),int(b),int(c)))

def conn(s1, s2):
    ss1 = set(s1)
    for (rotindex, rot) in enumerate(rots):
        s2r = rotlist(s2, rot)
        for (x1, y1, z1) in s1:
            for (x2, y2, z2) in s2r:
                (dx, dy, dz) = (x2 - x1, y2 - y1, z2 - z1)
                if len(ss1 & {(x - dx, y - dy, z - dz) for (x, y, z) in s2r}) >= 12:
                    return (rotindex, (dx, dy, dz))
    return None

beacons = set()
active = [scanners[0]]
scanner_locations = [(0,0,0)]
unconnected = scanners[1:]

while active:
    s1 = active.pop()
    i = 0
    while i < len(unconnected):
        if (match := conn(s1, unconnected[i])) is not None:
            (rotindex, (dx, dy, dz)) = match
            scanner_locations.append((dx,dy,dz))
            new = unconnected.pop(i)
            new = rotlist(new, rots[rotindex])
            new = [(x - dx, y - dy, z - dz) for (x,y,z) in new]
            active.append(new)
        else:
            i += 1
    beacons |= set(s1)

part2 = 0
for (x1, y1, z1) in scanner_locations:
    for (x2, y2, z2) in scanner_locations:
        part2 = max(part2, abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1))

print(f"part 1: {len(beacons)}")
print(f"part 2: {part2}")
