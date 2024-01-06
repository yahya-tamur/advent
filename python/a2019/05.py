from common import gp
from intcode import execute

input = [int(i) for i in gp().split(',')]
print(f"part 1: {execute(input.copy(), [1])[-1] }")
print(f"part 2: {execute(input, [5])[0]}")
