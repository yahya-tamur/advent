from problem import gpl
from collections import defaultdict
import heapq

edg = defaultdict(list)
coedg = defaultdict(list)
vals = set()

for line in gpl():
    edg[line[5]].append(line[36])
    coedg[line[36]].append(line[5])
    vals |= {line[5], line[36]}

start = [v for v in vals if not coedg[v]]
heapq.heapify(start)

p1 = ''
while start:
    a = heapq.heappop(start)
    if a in p1 or not all((x in p1 for x in coedg[a])):
        continue
    p1 += a
    for v in edg[a]:
        heapq.heappush(start,v)

print(f"part 1: {p1}")

workers = [0]*5

finished = set()
inprogress = set()
available = [v for v in vals if not coedg[v]]
heapq.heapify(available)

for time in range(90*len(vals)):
    for (p, t) in list(inprogress):
        if t <= time:
            finished.add(p)
            for v in edg[p]:
                if all((w in finished for w in coedg[v])):
                    heapq.heappush(available, v)
            inprogress.remove((p, t))

    if len(finished) == len(vals):
        print(f"part 2: {time}")
        break; # here?

    for i in range(5):
        if workers[i] > time:
            continue

        if not available:
            continue

        a = heapq.heappop(available)
        time_ = time + 60 + ord(a) - ord('A') + 1

        inprogress.add((a, time_))

        workers[i] = time_


