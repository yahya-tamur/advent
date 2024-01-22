from problem import gpl
from collections import defaultdict

m = defaultdict(lambda:'.')

for line in gpl():
    l, r = line.split(', ')
    a = int(l[2:])
    b = int(r[2:r.find('.')])
    c = int(r[r.rfind('.')+1:])
    if l[0] == 'x':
        for y in range(b,c+1):
            m[a+1j*y] = '#'
    else:
        for x in range(b,c+1):
            m[1j*a+x] = '#'
    if c <= b:
        print('nooo!!')

y0, y1 = int(min(z.imag for z in m)), int(max(z.imag for z in m))


active = [500]
m[500] = '|'

for a in active:
    if m[a] in '~#':
        continue
    m[a] = '|'
    while m[a+1j] in '.|' and a.imag <= y1:
        a += 1j
        m[a] = '|'
    if a.imag == y1+1:
        continue
    l, r = a, a
    while m[l] in '|.' and m[l+1j] in '#~':
        m[l] = '|'
        l -= 1
    while m[r] in '|.' and m[r+1j] in '#~':
        m[r] = '|'
        r += 1
    if m[l+1j] not in '#~':
        active.append(l)
    if m[r+1j] not in '#~':
        active.append(r)
    if m[l] == '#' and m[r] == '#':
        for i in range(int(l.real)+1, int(r.real)):
            m[i+l.imag*1j] = '~'
        active.append(a-1j)


print(f"part 1: {sum((c in '~|' for i, c in m.items() if int(i.imag) in range(y0, y1+1)))}")
print(f"part 2: {sum((c == '~' for i, c in m.items() if int(i.imag) in range(y0, y1+1)))}")


