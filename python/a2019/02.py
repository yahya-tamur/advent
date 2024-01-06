from common import gp
from intcode import run

code = [int(i) for i in gp().strip().split(',')]

code_ = [code[0], 12, 2] + code[3:]
list(run(code_,[]))
print(f"part 1: {code_[0]}")

for i in range(100):
    for j in range(100):
        code = [int(i) for i in gp().strip().split(',')]
        code_ = [code[0], i, j] + code[3:]
        list(run(code_,[]))
        if code_[0] == 19690720:
            print(f"part 2: {100*i + j}")

