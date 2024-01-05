from common import get_problem_lines

# 🌟🌟🌟

def get_ans(line):
    i = next((c for c in line if c.isdigit()))
    j = next((c for c in line[::-1] if c.isdigit()))
    return int(i)*10 + int(j)

ans1, ans2 = 0, 0
for line in get_problem_lines():
    ans1 += get_ans(line)
    for i, num in enumerate(['one', 'two', 'three', 'four', 'five', 'six', \
            'seven', 'eight', 'nine']):
        line = line.replace(num, f"{num}{i+1}{num}")
    ans2 += get_ans(line)

print(f"part 1: {ans1}")
print(f"part 2: {ans2}")
