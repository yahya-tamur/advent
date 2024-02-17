from problem import gpl

instrs = []
for line in gpl():
    line = line.replace(',', '')
    words = line.split(' ')
    if not words[-1].isalpha():
        words[-1] = int(words[-1])
    instrs.append(words)

def solve(a):
    r = {'a': a, 'b': 0}
    pc = 0

    while pc in range(len(instrs)):
        instr, *args = instrs[pc]

        match instr:
            case 'hlf':
                r[args[0]] //= 2
            case 'tpl':
                r[args[0]] *= 3
            case 'inc':
                r[args[0]] += 1
            case 'jmp':
                pc += args[0]
                continue
            case 'jie':
                if r[args[0]] % 2 == 0:
                    pc += args[1]
                    continue
            case 'jio':
                if r[args[0]] == 1:
                    pc += args[1]
                    continue
        pc += 1
    return r['b']

print(f"part 1: {solve(0)}")
print(f"part 2: {solve(1)}")
