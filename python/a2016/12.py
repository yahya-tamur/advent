# Input looked pretty easy to decompile but the program ran
# fast enough without doing that.

from problem import gpl

def solve(part):
    instrs = list()
    regs = dict()

    for line in gpl():
        words = line.split(' ')
        for w in words[1:]:
            if w.isalpha():
                regs[w] = 0
            else:
                regs[w] = int(w)
        instrs.append(tuple(words))

    pc = 0

    regs['c'] = part

    while pc < len(instrs):
        instr, *r = instrs[pc]

        match instr:
            case 'cpy':
                regs[r[1]] = regs[r[0]]
            case 'inc':
                regs[r[0]] += 1
            case 'dec':
                regs[r[0]] -= 1
            case 'jnz':
                if regs[r[0]] != 0:
                    pc += regs[r[1]]
                    continue
        pc += 1

    return regs['a']

print(f"part 1: {solve(0)}")
print(f"part 2: {solve(1)}")

