from common import gp
from sys import exit

code = [int(i) for i in gp().strip().split(',')]
code[1] = 12
code[2] = 2
c = 0
while True:
    match code[c]:
        case 1:
            code[code[c+3]] = code[code[c+1]] + code[code[c+2]]
            c += 4
        case 2:
            code[code[c+3]] = code[code[c+1]] * code[code[c+2]]
            c += 4
        case 99:
            break
        case x:
            print(x, code)
print(f"part 1: {code[0]}")

for i in range(100):
    for j in range(100):
        code = [int(i) for i in gp().strip().split(',')]
        code[1] = i
        code[2] = j
        c = 0
        while True:
            match code[c]:
                case 1:
                    code[code[c+3]] = code[code[c+1]] + code[code[c+2]]
                    c += 4
                case 2:
                    code[code[c+3]] = code[code[c+1]] * code[code[c+2]]
                    c += 4
                case 99:
                    break
                case x:
                    break
        if code[0] == 19690720:
            print(f"part 2: {100*i + j}")

