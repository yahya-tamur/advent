from problem import get_problem_lines
input = [list(line) for line in get_problem_lines()]

slopes = [1, 3, 5, 7]
ans = [0,0,0,0,0]
for (s, slope) in enumerate(slopes):
    for i in range(1,len(input)):
        if input[i][slope*i % len(input[0])] == '#':
            ans[s] += 1
for j in range(0,len(input)//2):
    if input[2*j][j % len(input[0])] == '#':
        ans[4] += 1

print(f"part 1: {ans[1]}")
print(f"part 2: {ans[0]*ans[1]*ans[2]*ans[3]*ans[4]}")
