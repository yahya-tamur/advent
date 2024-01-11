from intcode import interact, get_code

code = get_code()

_, sv = interact(code)

known = dict()
codirs = {1: 1, -1: 2, 1j: 3, -1j: 4}

current = 0
dir = 1

start = True

#good enough (thankfully)
while start or (current, dir) != (0, 1):
    start = False
    new = current + dir
    resp = sv(codirs[dir])
    known[new] = resp[0]
    if resp[0]:
        current = new
        dir *= -1j
    else:
        dir *= 1j


from collections import deque

def bfs(start, goal):
    seen = set()
    active = deque([(start, 0)])

    while active:
        (pos, steps) = active.popleft()
        if pos == goal:
            return steps
        for d in [1,-1,1j,-1j]:
            if pos + d not in seen and pos + d in known and known[pos+d] != 0:
                seen.add(pos + d)
                active.append((pos + d, steps + 1))
    return steps

goal = next((i for i in known if known[i] == 2))
print(f"part 1: {bfs(0,goal)}")
print(f"part 2: {bfs(goal,0.5)}")
