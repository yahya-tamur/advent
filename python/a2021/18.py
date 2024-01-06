from problem import get_problem_lines

def tosn(s):
    return [int(c) if c.isdigit() else c for c in s]

def psn(sn):
    for c in sn:
        print(c,end='')
    print()

def explode(sn):
    depth = 0
    k = None
    for i in range(len(sn)):
        if sn[i] == '[':
            depth += 1
        if sn[i] == ']':
            depth -= 1
        if depth > 4 and isinstance(sn[i],int) and sn[i+1] == ',' and isinstance(sn[i+2],int) :
            k = i
            break
    if k == None:
        return (False, sn)
    for j in range(k-1,-1,-1):
        if isinstance(sn[j], int):
            sn[j] += sn[k]
            break
    for j in range(k+3,len(sn)):
        if isinstance(sn[j], int):
            sn[j] += sn[k+2]
            break
    sn = sn[:k-1] + [0] + sn[k+4:]
    return (True, sn)

def split(sn):
    k = None
    for (i, c) in enumerate(sn):
        if isinstance(c, int) and c >= 10:
            k = i
            break
    if k == None:
        return (False, sn)
    l, r = sn[k] // 2, (sn[k] - (sn[k] // 2 ))
    sn = sn[:k] + ['[',l ,',', r, ']'] + sn[k+1:]
    return (True, sn)

def add(sn1, sn2):
    return ['['] + sn1 + [','] + sn2 + [']']

def simplify(sn):
    while True:
        c, sn = explode(sn)
        if c:
            continue
        c, sn = split(sn)
        if not c:
            return sn

def magnitude(sn):
    k = 1
    ans = 0
    for c in sn:
        if c == '[':
            k = k * 3
        if c == ',':
            k = k // 3
            k = k * 2
        if c == ']':
            k = k // 2
        if isinstance(c, int):
            ans += k*c
    return ans

lines = [simplify(tosn(x)) for x in get_problem_lines()]


sn = lines[0]
for line in lines[1:]:
    sn = simplify(add(sn, line))
print(f'part 1: {magnitude(sn)}')

ans = 0
for i in range(len(lines)):
    for j in range(len(lines)):
        if i == j:
            continue
        ans = max(ans, magnitude(simplify(add(lines[i],lines[j]))))

print(f'part 2: {ans}')



