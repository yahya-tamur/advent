from common import get_problem_lines
input = [int(i) for i in get_problem_lines()]
print(f"part 1: {next((i*(2020-i) for i in input if 2020 - i in input))}")
print(f"part 2: {next((i*j*(2020-i-j) for i in input for j in input if 2020 - i - j in input))}")
