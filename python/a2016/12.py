from problem import gpl

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
            pc += regs[r[0]]
            continue
    pc += 1

print(f"part 1: {r['a']}")

