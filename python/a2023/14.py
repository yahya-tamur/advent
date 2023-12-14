from common import get_problem_lines
from copy import deepcopy

map = [list(line) for line in get_problem_lines(file="input")]
#should reduce memory usage
for i in range(len(map)):
    for j in range(len(map)):
        match map[i][j]:
            case '.':
                map[i][j] = 0
            case 'O':
                map[i][j] = 1
            case '#':
                map[i][j] = 2
            case _:
                print('noo')

def tilt(map,r): # 0 = north, 1 = west, 2 = south, 3 = east
    # map is square
    def ccw(i,j):
        return (len(map)-1-j,i)
    def get(map, i,j,r):
        for _ in range(r):
            (i,j) = ccw(i,j)
        return map[i][j]
    def set(map, i, j, r, val):
        for _ in range(r):
            (i,j) = ccw(i,j)
        map[i][j] = val

    for i in range(len(map)):
        for j in range(len(map)):
            if get(map,i,j,r) == 1:
                k = i
                while k > 0 and get(map,k-1,j,r) == 0:
                    k -= 1
                set(map,i,j,r,0)
                set(map,k,j,r,1)

def getans(map):
    ans = 0
    for (i, line) in enumerate(map):
        ans += (len(map) - i)*sum([c == 1 for c in line])
    return ans


ans1map = deepcopy(map)
tilt(ans1map, 0)
print(f"part 1:{getans(ans1map)}")

def tiltN(map, N):
    prevmaps = list()
    for i in range(N):
        prevmaps.append(deepcopy(map))

        for j in range(i):
            if prevmaps[j] == map:
                k = j + ((N - j) % (i - j))
                print(i, j, k)
                return prevmaps[k]

        for r in range(4):
            tilt(map,r)

print(f"part 2: {getans(tiltN(map,1000000000))}")
