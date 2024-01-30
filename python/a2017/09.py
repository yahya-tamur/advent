from problem import gp

garbage = False
depth = 0
p1 = 0
p2 = 0
unlem = False

for c in gp().strip():
    if unlem:
        unlem = False
        continue
    if c == '<' and not garbage:
        garbage = True
        continue
    if garbage:
        if c == '!':
            unlem = True
        elif c == '>':
            garbage = False
        else:
            p2 += 1
        continue
    if c == '{':
        depth += 1
    if c == '}':
        p1 += depth
        depth -= 1

print(f"part 1: {p1}")
print(f"part 2: {p2}")

