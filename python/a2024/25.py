from problem import get_problem, get_problem_lines, look
print(f"part 1: {sum(not any(n == '#' and m == '#' for (n, m) in zip(x, y)) for x in get_problem().split(2*chr(10)) for y in get_problem().split(2*chr(10))) // 2 }")
print(f"part 2: {0}")
