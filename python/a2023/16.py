from common import get_problem_lines

map = [list(line) for line in get_problem_lines()]

# didn't speed up as much as I thought it would.
r, l, u, d = 1, 2, 4, 8

def get_ans(init):
    active = [init]

    visited = [[0 for _ in line] for line in map]

    def move(i, j, dir):
        match dir:
            case 1:
                return ((i,j+1), r)
            case 2:
                return ((i,j-1), l)
            case 4:
                return ((i-1,j), u)
            case 8:
                return ((i+1,j), d)

    while(active):
        (i,j), dir = active.pop()
        if i < 0 or j < 0 or i >= len(map) or j >= len(map[0]):
            continue
        if dir & visited[i][j]:
            continue
        visited[i][j] |= dir
        match dir:
            case 1:
                if map[i][j] == '.' or map[i][j] == '-':
                    active.append(move(i,j,r))
                if map[i][j] == '|' or map[i][j] == '/':
                    active.append(move(i,j,u))
                if map[i][j] == '|' or map[i][j] == '\\':
                    active.append(move(i,j,d))
            case 2:
                if map[i][j] == '.' or map[i][j] == '-':
                    active.append(move(i,j,l))
                if map[i][j] == '|' or map[i][j] == '/':
                    active.append(move(i,j,d))
                if map[i][j] == '|' or map[i][j] == '\\':
                    active.append(move(i,j,u))
            case 4:
                if map[i][j] == '.' or map[i][j] == '|':
                    active.append(move(i,j,u))
                if map[i][j] == '-' or map[i][j] == '/':
                    active.append(move(i,j,r))
                if map[i][j] == '-' or map[i][j] == '\\':
                    active.append(move(i,j,l))
            case 8:
                if map[i][j] == '.' or map[i][j] == '|':
                    active.append(move(i,j,d))
                if map[i][j] == '-' or map[i][j] == '/':
                    active.append(move(i,j,l))
                if map[i][j] == '-' or map[i][j] == '\\':
                    active.append(move(i,j,r))

    ans = 0
    for line in visited:
        for s in line:
            if s:
                ans += 1
    return ans

print(f"part 1: {get_ans(((0,0),r))}")

part2 = 0
for i in range(len(map)):
    part2 = max(part2, get_ans(((i,0), r)))
    part2 = max(part2, get_ans(((len(map)-1,0), l)))
for j in range(len(map[0])):
    part2 = max(part2, get_ans(((0,j), d)))
    part2 = max(part2, get_ans(((0,len(map[0])-1), u)))

print(f"part 2: {part2}")

    
