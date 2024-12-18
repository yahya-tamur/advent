from problem import get_problem, get_problem_lines
import heapq as h

N = 70

blocks = []
for i, line in enumerate(get_problem_lines()):
    l, r = line.split(',')
    blocks.append(int(l)+1j*int(r))

def solve(n):
    m = {i+1j*j: '.' for i in range(N+1) for j in range(N+1)}
    for b in blocks[:n]:
        m[b] = '#'

    states = [(0, "0")]
    seen = dict()
    while states:
        cost, s = h.heappop(states)
        s = complex(s)
        if seen.get(s, 999999999999999) <= cost:
            continue
        seen[s] = cost
        if s == N+1j*N:
            return cost
            break
        for d in (1, -1, 1j, -1j):
            if m.get(s+d, '#') == '.':
                h.heappush(states, (cost+1, str(s+d)))

    return -1

print(f"part 1: {solve(1024)}")

l = 0
r = len(blocks)
while r - l > 1:
    if solve((l+r)//2) == -1:
        r = (l+r) // 2
    else:
        l = (l+r) // 2

# solve(l) works, solve(l+1) doesn't,
# blocks[:l] works, blocks[:l+1]  doesn't.
z = blocks[l]
print(f"part 2: {str(int(z.real)) + ',' + str(int(z.imag))}")

