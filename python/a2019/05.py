from common import gp
from intcode import run
from collections import deque

input = [int(i) for i in gp().split(',')]
print(f"part 1: {deque(run(input.copy(), [1]),maxlen=1)[0] }")
print(f"part 2: {next(run(input, [5]))}")
