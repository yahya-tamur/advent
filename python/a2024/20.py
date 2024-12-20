from problem import get_problem, get_problem_lines, look

pl = get_problem_lines()
m = dict()

start = 0
for i in range(len(pl)):
    for j in range(len(pl[0])):
        z, c = i+1j*j, pl[i][j]
        if c == '#':
            m[z] = '#'
            continue
        m[z] = '.'
        if c == 'S':
            start = z

path = [start, next(start+d for d in (1,-1,1j,-1j) if m[start+d] == '.')]
ended = False

while not ended:
    z = path[-1]
    ended = True
    for z_ in (z+1, z-1, z+1j, z-1j):
        if z_ != path[-2] and m[z_] == '.':
            path.append(z_)
            ended = False
            break

def man(z, z_):
    return int(abs(z.real - z_.real) + abs(z.imag - z_.imag))

ans1, ans2 = 0, 0

for i in range(len(path)):
    z = path[i]
    for j in range(i+100, len(path)):
        if j - i - (l := man(z, path[j])) < 100:
            continue
        ans1 += l <= 2
        ans2 += l <= 20

print(f"part 1: {ans1}")
print(f"part 2: {ans2}")
