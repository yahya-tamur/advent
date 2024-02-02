from problem import gpl
from collections import defaultdict

parts = list()
for line in gpl():
    parts.append([])
    for pva in line.split('<')[1:]:
        parts[-1].append([])
        for c in pva[:pva.find('>')].split(','):
            parts[-1][-1].append(int(c))

_, p1 = min(( (sum((abs(c) for c in part[2])), i) for i, part in enumerate(parts) ))
print(f"part 1: {p1}")

# A naive estimate of 2(max |position|) iterations was a bit too slow.

# will reorder parts!
def done(parts):
    for k in range(3):
        parts.sort(key=lambda part: (part[2][k], part[0][k]))
        for i in range(len(parts)-1):
            if parts[i+1][0][k] < parts[i][0][k]:
                return False
    return True

while not done(parts):
    for _ in range(100):
        seen = defaultdict(int)

        parts_ = dict() # loc -> (vel, acc)
        for [x, y, z], [vx, vy, vz], [ax, ay, az] in parts:
            vx_, vy_, vz_ = vx + ax, vy + ay, vz + az
            x_, y_, z_ = x + vx_, y + vy_, z + vz_
            seen[(x_, y_, z_)] += 1
            parts_[(x_, y_, z_)] = ([vx_, vy_, vz_], [ax, ay, az])

        parts = [ [p, *parts_[p]] for p, n in seen.items() if n == 1 ]




print(f"part 2: {len(parts)}")

