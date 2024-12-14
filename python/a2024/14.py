from problem import get_problem, get_problem_lines

vx = []
vy = []

x = []
y = []
locs = []

for line in get_problem_lines():
    x.append(int(line[line.find('=')+1:line.find(',')]))
    y.append(int(line[line.find(',')+1:line.find(' ')]))

    vx.append(int(line[line.rfind('=')+1:line.rfind(',')]))
    vy.append(int(line[line.rfind(',')+1:]))


w = open('out', 'w')

for tim in range(200000):
    if tim == 100:
        qs = [0, 0, 0, 0]

        for i in range(len(x)):
            if x[i] == 50 or y[i] == 51:
                continue
            qs[ (x[i] < (50))*2 + (y[i] < (51))] += 1
        from math import prod
        print(f"part 1: {prod(qs)}")

    for i in range(len(x)):
        x[i] = (x[i] + vx[i]) % 101
        y[i] = (y[i] + vy[i]) % 103

    pts = {(x[i], y[i]) for i in range(len(x))}
    # whyy??
    if len(pts) == len(x):

        s = ""
        for i in range(101):
            for j in range(103):
                s += 'c' if (i,j) in pts else ' '
            s += '\n'

        #print(s)
        print(f"part 2: {tim+1}")
        exit()




