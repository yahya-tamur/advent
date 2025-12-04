from problem import get_problem, get_problem_lines, look
from time import time

grid = {i+1j*j for i, line in enumerate(get_problem_lines()) for j, c in enumerate(line) if c == '@'}

dirs = (1,-1,1j,-1j,1+1j,1-1j,-1+1j,-1-1j)

print(f"part 1: {sum(sum((z+d in grid) for d in dirs) < 4 for z in grid)}")

start_num = len(grid)

stack = list(grid)
#stackset = set(grid)

while stack:
    z = stack.pop()
    if z not in grid:
        continue
    #stackset.remove(z)
    if len( w := [z+d for d in dirs if z+d in grid]) < 4:
        grid.remove(z)
        # adding duplicates to the stack was (slightly) faster than keeping
        # a set of what's in the stack to prevent that.

        # I think it's because it's better to do DFS, not BFS for this problem.

        for ww in w:
            #if ww not in stackset:
            stack.append(ww)
                #stackset.add(ww)

print(f"part 2: {start_num - len(grid)}")
