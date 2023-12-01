from common import get_problem

dots = set()
folds = list()
for line in get_problem(2021,13).split('\n'):
    if not line:
        continue
    if (k := line.find('=')) != -1:
        folds.append((line[k-1], int(line[k+1:])))
    else:
        (l,r) = line.split(',')
        dots.add((int(l),int(r)))

first = True
for (d, s) in folds:
    fdots = set()
    for (r, c) in dots:
        if d == 'x':
            fdots.add((min(r, 2*s-r), c))
        else:
            fdots.add((r,min(c,2*s-c)))
    dots = fdots
    if first:
        print(f'part 1: {len(dots)}')
        first = False

(n, m) = (max(x[0] for x in dots)+1, max(x[1] for x in dots)+1)

board = [[' ' for _ in range(m)] for _ in range(n) ]
for (r, c) in dots:
    board[r][c] = '#'

print('part 2:')
for c in range(m):
    for r in range(n):
        print(board[r][c], end='')
    print()
