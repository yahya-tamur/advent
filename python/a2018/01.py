from problem import gpl

print(f"part 1: {sum((int(i) for i in gpl()))}")

l = [int(i) for i in gpl()]
seen = {l[0]}
i = 1
lastseen = l[0]
while True:
    n = lastseen + l[i]
    if n in seen:
        print(f"part 2: {n}")
        break
    lastseen = n
    seen.add(n)
    i = (i+1) % len(l)
