from problem import gp

p1, p2 = 0, None
for i, c in enumerate(gp().strip()):
    p1 += 2*(c == '(') - 1
    if p1 == -1 and p2 is None:
        p2 = i + 1

print(f"part 1: {p1}")
print(f"part 2: {p2}")
