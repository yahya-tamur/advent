from problem import gpl
import heapq

depth = int(gpl()[0].split(' ')[1])
x, y = eval(gpl()[1].split(' ')[1])

# Did not get the correct answer with 50 !
buffer = 200

m = [[0] * (y+buffer) for _ in range(x+buffer)]

for xx in range(1, x+buffer):
    m[xx][0] = (xx*16807 + depth) % 20183

for yy in range(1, y+buffer):
    m[0][yy] = (yy*48271 + depth) % 20183

for xx in range(1,x+buffer):
    for yy in range(1,y+buffer):
        if xx == x and yy == y:
            m[xx][yy] = depth % 20183
        else:
            m[xx][yy] = (m[xx-1][yy] * m[xx][yy-1] + depth) % 20183

print(f"part 1: {sum((sum((a % 3 for a in line[:y+1])) for line in m[:x+1])) - (m[x][y] % 3)}")

# Why does it take so long?
active = [(0, 0, 0, 1)]
seen = set()
while active:
    (steps, xx, yy, tool) = heapq.heappop(active)
    if (xx, yy, tool) in seen:
        continue
    seen.add((xx, yy, tool))
    if xx == x and yy == y and tool == 1:
        print(f"part 2: {steps}")
        break
    for xx_, yy_ in [(xx+1, yy), (xx-1, yy), (xx, yy+1), (xx, yy-1)]:
        if xx_ < 0 or xx_ >= len(m) or yy_ < 0 or yy_ >= len(m[0]):
            continue
        if m[xx][yy] % 3 == tool:
            continue
        heapq.heappush(active, (steps+1, xx_, yy_, tool))
    heapq.heappush(active, (steps+7, xx, yy, ({0,1,2} - {tool, m[xx][yy] % 3}).pop()))
