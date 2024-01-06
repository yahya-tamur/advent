from problem import get_problem_lines

lines = [line.split(' ') for line in get_problem_lines()]
sections = [lines[i:i+18] for i in range(0,len(lines),18)]

stack = []
constraints = [] # (i,n,j) means w[i] + n = w[j] i < j.

for (i, section) in enumerate(sections):
    if section[4][2] == "1":
        stack.append((i,section[15][2]))
    else:
        (index, num) = stack.pop()
        constraints.append((index, int(num) + int(section[5][2]), i))

ans1, ans2 = ["9" for _ in range(14)], ["1" for _ in range(14)]
for (i, n, j) in constraints:
    if n > 0:
        ans1[i] = str(9 - n)
        ans2[j] = str(1+n)
    else:
        ans1[j] = str(9 + n)
        ans2[i] = str(1-n)

print(f"part 1: {''.join(ans1)}")
print(f"part 2: {''.join(ans2)}")
