from problem import gp

serial = int(gp().strip())

m = [[0 for _ in range(300)] for _ in range(300)]

for x in range(300):
    for y in range(300):
        rid = x + 1 + 10
        pl = rid*(rid * (y+1) + serial)
        pl = (pl // 100) % 10
        m[x][y] = pl - 5

from time import time
def max_square_sum(m, max_square=None):
    if max_square == None:
        max_square=len(m)
    #h[i][j][k] = value of k x k square starting at (i,j)
    h = [[ [0, v] for v in line] for line in m]

    besti = (0,0,0)
    best = 0
    for k in range(2, max_square+1):
        for i in range(len(m)-k+1):
            for j in range(len(m)-k+1):
                h[i][j].append(h[i+1][j][k-1] + h[i][j+1][k-1] - h[i+1][j+1][k-2] + m[i][j] + m[i+k-1][j+k-1])
                if h[i][j][k] > best:
                    best = h[i][j][k]
                    besti = (i,j,k)
    return besti

def format_ans(ans, part):
    if part == 1:
        return f"{ans[0]+1},{ans[1]+1}"
    return f"{ans[0]+1},{ans[1]+1},{ans[2]}"

print(f"part 1: {format_ans(max_square_sum(m, 3), 1)}")
print(f"part 2: {format_ans(max_square_sum(m), 2)}")
