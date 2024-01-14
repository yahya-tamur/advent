from intcode import get_code, execute
from collections import defaultdict

# Interesting problem!!

init = execute(get_code(), [])

grid = [list(l) for l in ''.join((chr(c) for c in init)).split('\n')]

dm = {i + j*1j: c for i, line in enumerate(grid) for j, c in enumerate(line) if c != '.'}

xes = {x for x in dm if all((x + d in dm for d in [1, -1, 1j, -1j]))}
print(f"part 1: {int(sum((x.real * x.imag for x in xes)))}")

curr = next((z for z in dm if dm[z] in ['^', '<', 'v', '>']))
dir = {'^': -1, '<': -1j, 'v': 1, '>': 1j}[dm[curr]]

# first, get path. assume you always take longest roads possible.
instrs = list()
while True:
    # turn
    if curr + 1j*dir in dm:
        instrs.append('L')
        dir *= 1j
    elif curr - 1j*dir in dm:
        instrs.append('R')
        dir *= -1j
    else:
        break
    instrs.append(0)
    # move as much as possible
    while curr + dir in dm:
        curr += dir
        instrs[-1] += 1

instrs_ = list()
for instr in instrs:
    if type(instr) == int:
        if instr < 9:
            instrs_.append(str(instr))
        elif instr < 18:
            instrs_.append('9')
            instrs_.append(str(instr - 9))
        else:
            print('long line :(')
    else:
        instrs_.append(instr)
instrs = instrs_

def constrict(instrs, newletter):
    phrasecount = defaultdict(lambda: (0, set()))
    for i in range(len(instrs)):
        for j in range(i+2, min(len(instrs),i+10)+1):
            if all(( c in 'LR0123456789' for c in instrs[i:j] )):
                num, occupied = phrasecount[tuple(instrs[i:j])]
                if all(( x not in occupied for x in range(i,j) )):
                    phrasecount[tuple(instrs[i:j])] = (num + 1, occupied | set(range(i,j)))
    _, phrase = max(( ((len(name)-1)*(num-1), name) for (name, (num, _o)) in phrasecount.items() ))
    i = 0
    while i < len(instrs):
        if tuple(instrs[i:i+len(phrase)]) == phrase:
            instrs = instrs[:i] + [newletter] + instrs[i+len(phrase):]
        i += 1

    return (instrs, phrase)

# I wouldn't be surprised if this doesn't get the right answer with a different
# input. It's a greedy algorithm -- choosing A, then B, then C. Since there are
# even longer substrings that save more characters, but we don't allow long
# movement functions, it's probably essentially randomly picking A and B.

# It also doesn't really make sure the final instrs doesn't contain anything
# but function calls.

instrs, a = constrict(instrs, 'A')
instrs, b = constrict(instrs, 'B')
instrs, c = constrict(instrs, 'C')

def intercalate(l, sep):
    ans = list()
    for i in l[:-1]:
        ans.extend(i)
        ans.append(sep)
    if l:
        ans.extend(l[-1])
    return ans

code = get_code()
code[0] = 2
programs = [intercalate(list(l), ',') for l in [instrs, a, b, c, 'n']]
resp = execute(code, map(ord, intercalate(programs, '\n') + ['\n']))

print(f"part 2: {resp[-1]}")
