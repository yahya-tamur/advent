from problem import gpl

pl = gpl()

chrs = [[0]*256 for _ in pl[0]]
for line in gpl():
    for i, c in enumerate(line):
        chrs[i][ord(c)] += 1

p1, p2 = '', ''
for ch in chrs:
    _, c1 = max((n, c) for c, n in enumerate(ch))
    p1 += chr(c1)
    _, c2 = min((n, c) for c, n in enumerate(ch) if n != 0)
    p2 += chr(c2)

print(f"part 1: {p1}")
print(f"part 2: {p2}")




