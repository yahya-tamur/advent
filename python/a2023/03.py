from common import get_problem
from collections import defaultdict


s = [list(line) + ['.'] for line in get_problem().split('\n') if line]
s += [['.']*len(s[0])]

partsum = 0

gears = defaultdict(list)

for row, line in enumerate(s):
    i = 0
    while i < len(line):
        if line[i].isdigit():
            j = i
            while line[j].isdigit():
                j += 1
            num = int(''.join(line[i:j]))

            adj = [(row,i-1),(row,j)] + [(row-1,k) for k in range(i-1,j+1)] + \
                    [(row+1,k) for k in range(i-1,j+1)]

            for (i_, j_) in adj:
                if s[i_][j_] != '.':
                    gears[(i_,j_)] = gears[(i_,j_)] + [num]

            if any([s[i_][j_] != '.' for (i_, j_) in adj]):
                partsum += num

            i = j
        i += 1

print(f'part 1: {partsum}')

gearsum = 0
for gear in gears.values():
    if len(gear) == 2:
        gearsum += gear[0] * gear[1]

print(f'part 2: {gearsum}')
