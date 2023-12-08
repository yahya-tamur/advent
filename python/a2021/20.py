from common import get_problem_lines

s = get_problem_lines()

code = [1 if c == '#' else 0 for c in s[0]]
s = s[1:]
s = [[0] * 60 + [1 if c == '#' else 0 for c in line] + [0] * 60 for line in s]
for _ in range(60):
    s.insert(0,[0 for _ in s[0]])
    s.append([0 for _ in s[0]])

def get_code(i,j):
    if i == 0:
        i += 1
    if j == 0:
        j += 1
    if i == len(s)-1:
        i -= 1
    if j == len(s[0])-1:
        j -= 1
    n = 64*(4*s[i-1][j-1] + 2*s[i-1][j] + s[i-1][j+1]) + \
            8*(4*s[i][j-1] + 2*s[i][j] + s[i][j+1]) + \
            4*s[i+1][j-1] + 2*s[i+1][j] + s[i+1][j+1]
    return code[n]

def iterate(n):
    global s
    for _ in range(n):
        s = [[get_code(i,j) for j in range(len(s[0]))] for i in range(len(s))]

    n = 0
    for line in s:
        n += sum(line)
    return n

print(f"part 1: {iterate(2)}")
print(f"part 2: {iterate(48)}")
