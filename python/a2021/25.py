from problem import get_problem_lines

map = [list(line) for line in get_problem_lines()]
map_ = [list(line) for line in get_problem_lines()]
tmp = [list(line) for line in get_problem_lines()]

def step(map, map_, tmp):
    for i in range(len(map)):
        for j in range(len(map[0])):
            tmp[i][j] = map[i][j]
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == '.':
                if map[i][j-1] == '>':
                    tmp[i][j] = '>'
                    tmp[i][j-1] = '.'
    for i in range(len(map)):
        for j in range(len(map[0])):
            map_[i][j] = tmp[i][j]
    for i in range(len(map)):
        for j in range(len(map[0])):
            if tmp[i][j] == '.':
                if tmp[i-1][j] == 'v':
                    map_[i][j] = 'v'
                    map_[i-1][j] = '.'

i = 0
while True:
    i += 1
    step(map, map_,tmp)
    if map == map_:
        break
    i += 1
    step(map_, map,tmp)
    if map == map_:
        break

print(f"part 1: {i}")


        


