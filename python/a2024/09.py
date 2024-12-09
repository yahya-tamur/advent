from problem import get_problem, get_problem_lines

spaces = []
a = []

space = False
ix = 0

for n in get_problem()[:-1]:
    n = int(n)
    if space == False:
        for _ in range(n):
            a.append(ix)
        ix += 1
    else:
        for _ in range(n):
            spaces.append(len(a))
            a.append(-1)
    space = not space

si = 0

while si < len(spaces) and spaces[si] < len(a):
    l = a.pop()
    while l == -1:
        l = a.pop()
    if spaces[si] > len(a):
        break
    a[spaces[si]] = l
    si += 1

print(f"part 1: {sum(i*v for i, v in enumerate(a))}")

a = []
spaces = []

space = False
ix = 0

files = []

for n in get_problem()[:-1]:
    n = int(n)
    if space == False:
        files.append((len(a), ix, n))
        for _ in range(n):
            a.append(ix)
        ix += 1
    else:
        spaces.append((len(a), n))
        for _ in range(n):
            a.append(-1)
    space = not space

for (fstart, fname, flen) in files[::-1]:
    for i in range(len(spaces)):
        sstart, slen = spaces[i]
        if sstart > fstart:
            break
        if slen >= flen:
            for x in range(flen):
                a[fstart + x] = -1
                a[sstart + x] = fname
            spaces[i] = (sstart + flen, slen - flen)
            break

print(f"part 2: {sum(i*v for i, v in enumerate(a) if v != -1)}")

