from problem import get_problem, get_problem_lines

lines = get_problem_lines()

program = [int(x) for x in lines[-1][lines[-1].find(' ')+1:].split(',')]

def run(a):
    ip = 0
    abc = [a, 0, 0]

    def combo(n):
        if n < 4:
            return n
        else:
            return abc[n - 4]

    p1 = []
    while ip < len(program):
        match program[ip]:
            case 0:
                abc[0] = abc[0] >> combo(program[ip+1])
            case 1:
                abc[1] ^= program[ip+1]
            case 2:
                abc[1] = combo(program[ip+1]) & 7
            case 3:
                if abc[0] != 0:
                    ip = program[ip+1]
                    continue
            case 4:
                abc[1] ^= abc[2]
            case 5:
                p1.append(combo(program[ip+1]) & 7)
            case 6:
                abc[1] = abc[0] >> combo(program[ip+1])
            case 7:
                abc[2] = abc[0] >> combo(program[ip+1])
            case _:
                print('unknown opcode')
        ip += 2

    return p1

print(f"part 1: {','.join(str(x) for x in run(int(lines[0][lines[0].rfind(' '):])))}")

steps = []
for a in range(2 ** 10):
    steps.append(run(a)[0])


ll = [[i] for i in range(2 ** 10) if steps[i] == program[0]]


for k in program[1:]:
    ll_ = []
    for l in ll:
        current = l[-1] >> 3
        for i in range(8):
            if steps[(i << 7) + current] == k:
                ll_.append(l + [(i << 7) + current])

    ll = ll_

def recombine(l):
    i = l[0]
    d = 10

    for c in l[1:]:
        i += (c >> 7) << d
        d += 3

    return i

ans = float('inf')
for l in ll:
    i = recombine(l)
    if run(i) == program:
        ans = min(i, ans)

print(f"part 2: {ans}")
