from problem import gp

step = int(gp())

l = [0]
r = [0]

now = 0
for i in range(1,2017+1):
    for _ in range(step):
        now = r[now]
    l.append(now)
    r.append(r[now])
    l[r[now]] = i
    r[now] = i
    now = i
print(f"part 1: {r[2017]}")

i = 0
for j in range(1,50_000_000+1):
    i = ((i + step) % j)+1
    if i == 1:
        p2 = j

print(f"part 2: {p2}")
