
from problem import gpl

pl = gpl()

ip = int(pl[0].split(' ')[1])

instrs = list()

for n, line in enumerate(pl[1:]):
    instr, a, b, c = line.split(' ')

    match instr:
        case 'addr':
            exec(f"def i{n}(): r[{c}] = r[{a}] + r[{b}]")
        case 'addi':
            exec(f"def i{n}(): r[{c}] = r[{a}] + {b}")
        case 'mulr':
            exec(f"def i{n}(): r[{c}] = r[{a}] * r[{b}]")
        case 'muli':
            exec(f"def i{n}(): r[{c}] = r[{a}] * {b}")
        case 'banr':
            exec(f"def i{n}(): r[{c}] = r[{a}] & r[{b}]")
        case 'bani':
            exec(f"def i{n}(): r[{c}] = r[{a}] & {b}")
        case 'borr':
            exec(f"def i{n}(): r[{c}] = r[{a}] | r[{b}]")
        case 'bori':
            exec(f"def i{n}(): r[{c}] = r[{a}] | {b}")
        case 'setr':
            exec(f"def i{n}(): r[{c}] = r[{a}]")
        case 'seti':
            exec(f"def i{n}(): r[{c}] = {a}")
        case 'gtir':
            exec(f"def i{n}(): r[{c}] = int({a} > r[{b}])")
        case 'gtri':
            exec(f"def i{n}(): r[{c}] = int(r[{a}] > {b})")
        case 'gtrr':
            exec(f"def i{n}(): r[{c}] = int(r[{a}] > r[{b}])")
        case 'eqir':
            exec(f"def i{n}(): r[{c}] = int({a} == r[{b}])")
        case 'eqri':
            exec(f"def i{n}(): r[{c}] = int(r[{a}] == {b})")
        case 'eqrr':
            exec(f"def i{n}(): r[{c}] = int(r[{a}] == r[{b}])")
    instrs.append(eval(f"i{n}"))

ans = [0, 0]
for part in range(2):
    r = [0] * 6
    if part == 1:
        r[0] = 1

    # 🌟🌟🌟 
    # run the program enough to get the correct input register
    for _ in range(100):

        instrs[r[ip]]()

        r[ip] += 1

    # find out what's the correct input register
    equalsline = next((line for line in pl if 'eq' in line))
    inp = r[next((i for i in range(6) if equalsline.count(str(i)) == 1))]

    # actually get the answer
    from math import sqrt, ceil
    for i in range(1,ceil(sqrt(inp))):
        if inp % i == 0:
            ans[part] += i + (inp // i)

print(f"part 1: {ans[0]}")
print(f"part 2: {ans[1]}")
