from problem import gpl
from collections import defaultdict

#i -> times guard i wakes up or falls asleep
sch = defaultdict(list)

guard = -1

lines = gpl()
lines.sort() # chronological.

for line in lines:
    day = line[6:11]
    hour = line[12:14]
    minute = line[15:17]
    thing = line[19:]

    if 'Guard' in thing:
        guard = int(thing[7:thing.find(' ',7)])
    else:
        sch[guard].append((day, int(hour), int(minute)))

for sh in sch.values():
    sh.sort()

sleep = {i: list() for i in sch}

for i, sh in sch.items():
    for j in range(0, len(sh), 2):
        d, ah, am = sh[j]
        _, bh, bm = sh[j+1]
        if ah == bh:
            for m in range(am, bm):
                sleep[i].append((d, ah, m))
        else:
            for m in range(am, 60):
                sleep[i].append((d, 0, bm))
            for m in range(am, 60):
                sleep[i].append((d, bh, m))
            for h in range(ah+1, bh):
                for m in range(0, 60):
                    sleep[i].append((d, h, m))

_, sleptmost = max(((len(sl), i) for i, sl in sleep.items()))

sleepoverlap = defaultdict(int)

for _, _, m in sleep[sleptmost]:
    sleepoverlap[m] += 1

print(f"part 1: {sleptmost*max((v, k) for k, v in sleepoverlap.items())[1]}")

gm = defaultdict(int)

for i, sl in sleep.items():
    for _, _, m in sleep[i]:
        gm[(i, m)] += 1

_, (guard, minute) = max(((v, k) for k, v in gm.items()))
print(f"part 2: {guard*minute}")
