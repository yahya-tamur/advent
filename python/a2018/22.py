from problem import gpl
depth = int(gpl()[0].split(' ')[1])
x, y = eval(gpl()[1].split(' ')[1])


#print(depth, x, y)
#depth, x, y = 510, 10, 10

m = [[0] * (y+1) for _ in range(x+1)]

for xx in range(1, x+1):
    m[xx][0] = (xx*16807 + depth) % 20183

for yy in range(1, y+1):
    m[0][yy] = (yy*48271 + depth) % 20183

for xx in range(1,x+1):
    for yy in range(1,y+1):
        m[xx][yy] = (m[xx-1][yy] * m[xx][yy-1] + depth) % 20183

p1 = sum((sum((a % 3 for a in line)) for line in m)) - (m[x][y] % 3)


print(f"part 1: {p1}")
