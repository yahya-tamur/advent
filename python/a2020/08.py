from problem import gpl
from sys import exit

instrs = [[line[:3], int(line[3:])] for line in gpl()]

acc = 0
visited = set()
current = 0
while current not in visited:
    visited.add(current)
    ins, val = instrs[current]
    match ins:
        case 'nop':
            current += 1
        case 'acc':
            acc += val
            current += 1
        case 'jmp':
            current += val

print(f"part 1: {acc}")

for i in range(len(instrs)):
    match instrs[i][0]:
        case 'nop':
            instrs[i][0] = 'jmp'
        case 'jmp':
            instrs[i][0] = 'nop'
        case 'acc':
            continue

    acc = 0
    visited = set()
    current = 0
    while current not in visited:
        if current == len(instrs):
            print(f"part 2: {acc}")
            exit()
        visited.add(current)
        ins, val = instrs[current]
        match ins:
            case 'nop':
                current += 1
            case 'acc':
                acc += val
                current += 1
            case 'jmp':
                current += val

    match instrs[i][0]:
        case 'nop':
            instrs[i][0] = 'jmp'
        case 'jmp':
            instrs[i][0] = 'nop'
        case 'acc':
            continue
