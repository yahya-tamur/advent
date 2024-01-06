from problem import get_problem_lines
from collections import deque

map = [list(line) for line in get_problem_lines()]

def ns(ij):
    i, j = ij
    n, s, w, e = (i-1,j),(i+1,j),(i,j-1),(i,j+1)
    match map[i][j]:
        case '|':
            return [n,s]
        case '-':
            return [w,e]
        case 'L':
            return [n,e]
        case 'J':
            return [n,w]
        case '7':
            return [s,w]
        case 'F':
            return [s,e]
        case 'S':
            return [(ni, nj) for (ni, nj) in [n,s,w,e] if (i,j) in ns((ni,nj))]
        case _:
            return []

s = next(((i,j) for i in range(len(map)) for j in range(len(map[0])) if \
          map[i][j] == 'S' ))

integral = 0
pathlen = 0
def step(a, a_):
    global integral, pathlen
    integral += a[0] * (a_[1] - a[1])
    pathlen += 1
    return (a_, next(( a__ for a__ in ns(a_) if a__ != a)))

(a, a_) = step(s, ns(s)[0])

while a != s:
    a, a_ = step(a, a_)

print(f"part 1: {pathlen // 2}")
print(f"part 2: {abs(integral) - ((pathlen // 2) - 1)}")
