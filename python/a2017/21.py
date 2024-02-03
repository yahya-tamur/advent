from problem import gpl

# slip -> 8 slips
def perms(slip):
    grid = [list(l) for l in slip.split('/')]

    def rot(grid):
        grid_ = []
        for i in range(len(grid)):
            grid_.append([])
            for j in range(len(grid)):
                grid_[-1].append(grid[j][~i])
        return grid_
    def flip(grid):
        grid_ = []
        for i in range(len(grid)):
            grid_.append([])
            for j in range(len(grid)):
                grid_[-1].append(grid[i][~j])
        return grid_
    def to_slip(grid):
        return '/'.join([''.join(line) for line in grid])

    ans = set()
    for _ in range(2):
        grid = flip(grid)
        for _ in range(4):
            grid = rot(grid)
            ans.add(to_slip(grid))
    return ans

keys = dict()

for line in gpl():
    ll, r = line.split(' => ')
    for l in perms(ll):
        keys[l] = r

def iterate(grid, k):
    n = len(grid)
    blocks = n // k
    slips = list()
    for ii in range(0, n, k):
        for jj in range(0, n, k):
            slip = ''
            for i in range(ii,ii+k):
                for j in range(jj,jj+k):
                    slip += grid[i][j]
                slip += '/'

            slips.append(keys[slip[:-1]].split('/'))
    grid.clear()
    for i in range(blocks*(k+1)):
        grid.append(list())
        for j in range(blocks*(k+1)):
            s = (i // (k+1))*blocks + (j // (k+1))
            grid[-1].append(slips[s][i % (k+1)][j % (k+1)])
    return grid

def get_ans(grid):
    return sum(( sum((c == '#' for c in line)) for line in grid))


grid = [list(l) for l in '.#./..#/###'.split('/')]

for k in range(18):
    if len(grid) % 2 == 0:
        grid = iterate(grid, 2)
    elif len(grid) % 3 == 0:
        grid = iterate(grid, 3)
    if k == 4:
        print(f"part 1: {get_ans(grid)}")

print(f"part 2: {get_ans(grid)}")
