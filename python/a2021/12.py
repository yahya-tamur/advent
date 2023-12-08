from common import get_problem

c = dict()
for line in get_problem().split('\n'):
    if not line:
        continue
    (l, r) = line.split('-')
    if l not in c:
        c[l] = set()
    if r not in c:
        c[r] = set()
    c[l] |= {r}
    c[r] |= {l}

completed_paths = 0
paths = [['start']]

while paths:
    p = paths.pop()
    if p[-1] == 'end':
        completed_paths += 1
        continue
    for s in c[p[-1]]:
        if s.isupper() or s not in p:
            p_ = p.copy()
            p_.append(s)
            paths.append(p_)

print(f'part 1: {completed_paths}')

completed_paths = 0
paths = [(['start'], False)]

while paths:
    (p, b) = paths.pop()
    if p[-1] == 'end':
        completed_paths += 1
        continue
    for s in c[p[-1]]:
        if s.isupper() or s not in p:
            p_ = p.copy()
            p_.append(s)
            paths.append((p_,b))
        if s.islower() and s in p and not b and s not in {'start', 'end'}:
            p_ = p.copy()
            p_.append(s)
            paths.append((p_, True))

print(f'part 2: {completed_paths}')


