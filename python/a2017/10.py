from problem import gp
from knot_hash import run, knot_hash

lst = run([int(x) for x in gp().strip().split(',')])
print(f"part 1: {lst[0]*lst[1]}")

p2 = ""
for d in knot_hash(gp().strip()):
    p2 += hex(d)[2:].zfill(2)

print(f"part 2: {p2}")
