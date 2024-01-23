from problem import gp

inp = gp().strip()[1:-1]
print(inp)

stack = [[0]]

p2 = 0
current_length = 0

for c in inp:
    if c in 'NWSE':
        stack[-1][-1] += 1
        current_length += 1
        if current_length >= 1000:
            p2 += 1
    if c == '(':
        stack.append([0])
    if c == '|':
        current_length -= stack[-1][-1]
        stack[-1].append(0)
    if c == ')':
        current_length -= stack[-1][-1]
        l = stack.pop()
        if 0 in l:
            continue
        current_length += max(l)
        stack[-1][-1] += max(l)
    print(stack, current_length)


print(f"part 1: {stack[-1][-1]}")
print(f"part 2: {p2}")
