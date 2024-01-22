from problem import gp

def imm(op):
    def proc(instr, regs):
        l = list(regs)
        l[instr[3]] = op(regs[instr[1]], instr[2])
        return tuple(l)
    return proc

def reg(op):
    def proc(instr, regs):
        l = list(regs)
        l[instr[3]] = op(regs[instr[1]], regs[instr[2]])
        return tuple(l)
    return proc

def imm_reg(op):
    def proc(instr, regs):
        l = list(regs)
        l[instr[3]] = op(instr[1], regs[instr[2]])
        return tuple(l)
    return proc

ops = [ \
    imm(lambda a, b: a+b), reg(lambda a, b: a+b), \
    imm(lambda a, b: a*b), reg(lambda a, b: a*b), \
    imm(lambda a, b: a&b), reg(lambda a, b: a&b), \
    imm(lambda a, b: a|b), reg(lambda a, b: a|b), \
    imm_reg(lambda a, b: a), reg(lambda a, b: a), \
    imm(lambda a, b: int(a>b)), reg(lambda a, b: int(a>b)), \
    imm(lambda a, b: int(a==b)), reg(lambda a, b: int(a==b)), \
    imm_reg(lambda a, b: int(a>b)), imm_reg(lambda a, b: int(a==b)), \
]

tests, inputs = gp().split('\n\n\n\n')

p1 = 0

opcode_options = {i : set(range(16)) for i in range(16)}

tests = tests.split('\n\n')
for test in tests:
    before = eval(test[test.find('[')+1:test.find(']')])
    instr = eval(test[test.find('\n')+1:test.rfind('\n')].replace(' ', ','))
    after = eval(test[test.rfind('[')+1:test.rfind(']')])
    matches = {i for i, op in enumerate(ops) if op(instr, before) == after}
    p1 += len(matches) >= 3
    opcode_options[instr[0]] &= matches

print(f"part 1: {p1}")

opcode = dict()

while len(opcode) < 16:
    i, v = next(( (i, v.pop()) for (i, v) in opcode_options.items() if len(v) == 1))
    opcode[i] = v
    for i in opcode_options:
        opcode_options[i] -= {v}

regs = (0, 0, 0, 0)
for instr in inputs.strip().split('\n'):
    instr = eval(instr.replace(' ', ','))
    regs = ops[opcode[instr[0]]](instr, regs)

print(f"part 2: {regs[0]}")
