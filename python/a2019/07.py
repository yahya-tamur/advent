from common import gp
from intcode import run
from itertools import permutations
from collections import deque

code = [int(i) for i in gp().split(',')]
def run_seq(seq):
    val = 0
    for s in seq:
        val = next(run(code.copy(), [s, val]))
    return val

def run_seq2(phase):
    channels = [deque([x]) for x in phase]
    channels[0].append(0)

    def give_input(i):
        while True:
            yield(channels[i].popleft())

    machines = [run(code.copy(), give_input(i)) for i in range(5)]

    while True:
        for i in range(5):
            if (n := next(machines[i],None)) is not None:
                channels[(i+1)%5].append(n)
            else:
                return channels[0][0]



print(f"part 1: {max((run_seq(phase) for phase in permutations(range(5))))}")
print(f"part 2: {max((run_seq2(phase) for phase in permutations(range(5,10))))}")
