from problem import gpl

pos, vel = list(), list()

for line in gpl():
    def ft(fro, to):
        l = line.find(fro)
        r = line.find(to, l)
        return int(line[l+len(fro):r])
    x, y, z = ft('x=', ','), ft('y=', ','), ft('z=', '>')
    pos.append([x,y,z])
    vel.append([0,0,0])

p2pos, p2vel = pos.copy(), vel.copy()

for _n in range(1000):
    for i in range(len(pos)):
        for j in range(len(pos)):
            for c in range(3):
                if pos[i][c] < pos[j][c]:
                    vel[i][c] += 1
                    vel[j][c] -= 1
    for i in range(len(pos)):
        for c in range(3):
            pos[i][c] += vel[i][c]
    #print(n, pos, vel)

p1 = 0
for i in range(len(pos)):
    p, k = 0, 0
    for c in range(3):
        p += abs(pos[i][c])
        k += abs(vel[i][c])
    p1 += p*k

print(f"part 1: {p1}")

cycles = list()
for c in range(3):
    states = set()
    n = 0
    while True:
        state = tuple([p[c] for p in pos] + [v[c] for v in vel])
        if state in states:
            break
        states.add(state)
        for i in range(len(pos)):
            for j in range(len(pos)):
                if pos[i][c] < pos[j][c]:
                    vel[i][c] += 1
                    vel[j][c] -= 1
        for i in range(len(pos)):
            pos[i][c] += vel[i][c]
        n += 1
    cycles.append(n)

from math import lcm
print(f"part 2: {lcm(*cycles)}")
