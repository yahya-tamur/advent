from problem import get_problem, get_problem_lines, look

lines = get_problem_lines()

symbols = []

i = 0

while 'x' not in lines[i]:
    symbols.append(''.join(lines[i:i+4]).count('#'))
    i += 4

p1 = 0

for line in lines[i:]:
    l, *rr = line.split(' ')
    p1 += eval(l[:-1].replace('x','*')) >= sum(s*int(r) for s, r in zip(symbols, rr))

print(f"part 1: {p1}")
print(f"part 2: {0}")
