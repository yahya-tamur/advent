from problem import gp
from intcode import execute

code = [int(i) for i in gp().strip().split(',')]

print(f"part 1: {execute(code.copy(),[1])[0]}")
print(f"part 2: {execute(code,[2])[0]}")
