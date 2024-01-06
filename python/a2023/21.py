from problem import get_problem_lines

lines = get_problem_lines()
n, m = len(lines), len(lines[0])
map = {i + j*1j for i in range(n) for j in range(m) if lines[i][j] == '.'}
start = {i + j*1j for i in range(n) for j in range(m) if lines[i][j] == 'S'}
map |= start

ext = [-393, -262, -131, 0, 131, 262, 393]

extmap = {a + b + c*1j for a in map for b in ext for c in ext}

total = 26501365

init = total % 131

cycles = {x: -1 for x in [64, init, init+131, init+262]}

current = start
for k in range(1,max(cycles)+1):
    current = {a + b for a in current for b in [1, -1, 1j, -1j] if a + b in extmap}
    if k in cycles:
        cycles[k] = len(current)

# Uses interpolation idea I got from reddit

print(f"part 1: {cycles[64]}")

# want: q(-1) = cycles[init], q(0) = cycles[init+260], q[1] = cycles[init+520].
# answer = cycles[init + 260*(total // 260)] = q[total // 260 - 1]
# let A = cycles[init], B = cycles[init+260], C = cycles[init+520]
# ax^2 + bx + c:
# q(-1) = a - b + c = A
# q(0) = c = B
# q(1) = a + b + c = C

A, B, C = cycles[init], cycles[init+131], cycles[init+262]
a, b, c = ((A + C) // 2) - B, (C - A) // 2, B
n = (total // 131) - 1
print(f"part 2: {a*n*n + b*n + c}")
