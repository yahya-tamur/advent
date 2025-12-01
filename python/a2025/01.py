from problem import get_problem_lines

dial = 50
dial_ = 49

dirs = {'L': -1, 'R': 1}
ans1 = 0
ans2 = 0

for line in get_problem_lines():
    dial += dirs[line[0]]*int(line[1:])
    dial_ += dirs[line[0]]*int(line[1:])
    ans2 += abs(dial // 100) + abs(dial_ // 100)
    dial = dial % 100
    dial_ = dial_ % 100
    ans1 += dial == 0

print(f"part 1: {ans1}")
print(f"part 2: {((ans2 + (dial == 0))) // 2}")
