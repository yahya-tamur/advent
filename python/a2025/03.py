from problem import get_problem, get_problem_lines, look


def solve_line(line, digits):

    last_index = -1
    ans = 0

    for d in range(digits-1, -1, -1):
        li, i = max((line[i], -i) for i in range(last_index+1, len(line) - d))
        last_index = -i
        ans = 10*ans + li

    return ans

p1, p2 = 0, 0

for line in get_problem_lines():
    line = [int(x) for x in line]
    p1 += solve_line(line, 2)
    p2 += solve_line(line, 12)


print(f"part 1: {p1}")
print(f"part 1: {p2}")
