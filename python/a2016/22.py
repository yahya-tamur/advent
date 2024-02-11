from problem import gpl

pl = gpl()

i_used, i_avail = [pl[1].find(s) for s in ('Used', 'Avail')]

i_name = len('/dev/grid/node-')

used, avail = dict(), dict()

for line in pl[2:]:
    name = line[i_name:i_name+7]
    used[name] = int(line[i_used:i_used+3])
    avail[name] = int(line[i_avail:i_avail+4])

p1 = sum(used[n] != 0 and used[n] <= avail[m] for n in used for m in avail if m != n)
print(f"part 1: {p1}")

from collections import deque

grid = set()
start = None

for n in used:
    z = int(n[1:n.find('-')]) + 1j*int(n[n.find('y')+1:])
    if used[n] == 0:
        start = z
    if avail[n] + used[n] < 200:
        grid.add(z)

available = deque([(0, start, int(max(z.real for z in grid)))])

seen = set()

while available:
    steps, empty, target = available.popleft()

    if (empty, target) in seen:
        continue
    seen.add((empty, target))

    if target == 0:
        print(f"part 2: {steps}")
        break

    for d in (1,-1,1j,-1j):
        if empty + d not in grid:
            continue
        target_ = empty if empty + d == target else target
        available.append((steps + 1, empty + d, target_))
