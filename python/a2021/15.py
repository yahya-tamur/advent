from common import get_problem

input = get_problem(2021, 15)
#input = """1163751742
#1381373672
#2136511328
#3694931569
#7463417111
#1319128137
#1359912421
#3125421639
#1293138521
#2311944581"""

input = [[int(c) for c in row] for row in input.split("\n") if row.strip()]

(n, m) = (len(input), len(input[0]))

def minimize(n, m):
    costs = [[69 ** 12]*(m+2) for _ in range(n+2)]
    costs[0][1] = -input[0][0]

    for i in range(n):
        for j in range(m):
            costs[i+1][j+1] = input[i][j] + min(costs[i][j+1], costs[i+1][j])

    def min_around(i,j):
        return min(costs[i][j+1], costs[i+1][j], costs[i+2][j+1], costs[i+1][j+2]) + input[i][j]

    needs_updating = list()
    for i in range(n):
        for j in range(m):
            if costs[i+1][j+1] > min_around(i,j):
                needs_updating.append((i,j))

    while needs_updating:
        (i, j) = needs_updating.pop()
        if i == -1 or j == -1 or i == n or j == m:
            continue
        if costs[i+1][j+1] > min_around(i,j):
            costs[i+1][j+1] = min_around(i,j)
            needs_updating += [(i-1,j), (i,j-1), (i+1,j), (i,j+1)]

    return costs[n][m]


def round(i):
    return (i-1)%9 + 1

input = [[round(input[i % n][j % m] + (i // n) + (j // m)) for j in range(m*5)] for i in range(n*5)]
print(f"part 1: {minimize(n,m)}")
print(f"part 2: {minimize(5*n, 5*m)}")
