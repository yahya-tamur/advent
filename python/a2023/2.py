from common import get_problem_lines
from collections import defaultdict

ans1 = 0
ans2 = 0
for line in get_problem_lines(2023, 2):
    id = int(line[4:line.find(':')])
    line = line[line.find(':')+2:]
    d = defaultdict(int)
    for l in line.split('; '):
        for s in l.strip().split(', '):
            [l, r] = s.split(' ')
            d[r] = max(d[r], int(l))
    if d['red'] <= 12 and d['green'] <= 13 and d['blue'] <= 14:
        ans1 += id
    ans2 += d['red'] * d['green'] * d['blue']
print(f'part 1: {ans1}')
print(f'part 2: {ans2}')
        #d = { r: int(l) for s in l.strip().split(', ') for [l, r] in s.strip().split(' ')}
