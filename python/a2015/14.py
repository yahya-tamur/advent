from problem import gpl

speeds, travels, rests = [], [], []

p1 = 0
for line in gpl():
    words = line.split(' ')
    speed, travel, rest = int(words[3]), int(words[6]), int(words[-2])

    q, r = 2503 // (travel + rest), 2503 % (travel + rest)
    p1 = max(p1, q*travel*speed + min(travel, r)*speed)

    speeds.append(speed)
    travels.append(travel)
    rests.append(rest)

print(f"part 1: {p1}")

n = len(speeds)

locs = [0 for _ in range(n)]
pts = [0 for _ in range(n)]

for i in range(2503):
    for r in range(n):
        if i % (travels[r] + rests[r]) < travels[r]:
            locs[r] += speeds[r]
    m = max(locs)
    for r in range(n):
        if locs[r] == m:
            pts[r] += 1

print(f"part 2: {max(pts)}")


