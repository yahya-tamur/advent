from problem import get_problem, get_problem_lines, look

inp = get_problem()

symbols = [[x for x in line.split(' ') if x] for line in get_problem_lines()]

from math import prod

p1 = 0
for i in range(len(symbols[0])):
    if symbols[-1][i] == '*':
        p1 += prod(int(symbols[j][i]) for j in range(len(symbols)-1))
    else:
        p1 += sum(int(symbols[j][i]) for j in range(len(symbols)-1))
print(f"part 1: {p1}")

lines = get_problem_lines()

starts = [i for i in range(len(lines[-1])) if lines[-1][i] != ' ']
starts.append(len(lines[-1])+1)

p2 = 0
for i in range(len(starts)-1):
    l, r = starts[i], starts[i+1]
    op, current = (prod, 1) if lines[-1][l] == '*' else (sum, 0)
    for i in range(l, r-1):
        num = 0
        for j in range(len(lines)-1):
            if (w := lines[j][i]) != ' ':
                num = num*10 + int(w)
        current = op((current, num))
    p2 += current

print(f"part 2: {p2}")




