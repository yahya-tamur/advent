from problem import gpl

instrs = list()

rs = dict()

for line in gpl():
    instr, *r = line.split(' ')
    instrs.append([instr, *r])

    for r_ in r:
        if r_.isalpha():
            rs[r_] = 0
        else:
            rs[r_] = int(r_)

pc = 0
rs['a'] = 12

print(rs)

while pc < len(instrs):

    instr, *r = instrs[pc]
    match instr:
        case 'cpy':
            if r[1].isalpha():
                rs[r[1]] = rs[r[0]]
        case 'inc':
            rs[r[0]] += 1
        case 'dec':
            rs[r[0]] -= 1
        case 'jnz':
            if rs[r[0]] != 0:
                pc += rs[r[1]]
                continue
        case 'tgl':
            print('tgl')
            if (i := pc + rs[r[0]]) in range(len(instrs)):
                print("tgl", instrs[i][0])
                match instrs[i][0]:
                    case 'inc':
                        instrs[i][0] = 'dec'
                    case 'dec':
                        instrs[i][0] = 'inc'
                    case 'jnz':
                        instrs[i][0] = 'cpy'
                    case 'cpy':
                        instrs[i][0] = 'jnz'
                    case 'tgl':
                        instrs[i][0] = 'inc'
    pc += 1

print(f"part 1: {rs['a']}")



