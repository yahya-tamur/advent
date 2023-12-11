from common import get_problem_lines
map = [list(line) for line in get_problem_lines()]
print(map)

#steps = ...

#loo
#ns(i, j) -> list[]
def ns(i,j):
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
        case _:
            pass

print(ns(10,4))

#active = {i, j in surrounding of S if ns(i,j) includes surrounding of S}

...

