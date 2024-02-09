from problem import gpl

grid = [[False]*50 for _ in range(6)]

for line in gpl():
    if 'rect' in line:
        line = line[line.find(' ')+1:]
        n, m = line.split('x')
        n, m = int(n), int(m)
        for i in range(n):
            for j in range(m):
                grid[j][i] = True
    elif 'column' in line:
        line = line[line.find('=')+1:]
        col, by = line.split(' by ')
        col, by = int(col), int(by)
        col_ = [grid[i][col] for i in range(6)]
        for i in range(6):
            grid[(i+by)%6][col] = col_[i]
    elif 'row' in line:
        line = line[line.find('=')+1:]
        row, by = line.split(' by ')
        row, by = int(row), int(by)
        row_ = grid[row].copy()
        for i in range(50):
            grid[row][(i+by)%50] = row_[i]
print(f"part 1: {sum(sum(i) for i in grid)}")
print("part 2:")
for i in range(6):
    for j in range(50):
        print('#' if grid[i][j] else ' ', end='')
    print()
