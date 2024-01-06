from problem import gp
from intcode import execute, interact
from itertools import permutations

code = [int(i) for i in gp().split(',')]
def run_seq(phase):
    val = 0
    for p in phase:
        val = execute(code.copy(), [p, val])[0]
    return val

def run_seq2(phase):
    senders, receivers = list(), list()
    for i in phase:
        send, recv = interact(code.copy())
        send(i)
        senders.append(send)
        receivers.append(recv)

    senders[0](0)
    ans = 0
    while True:
        for i in range(5):
            if (n := next(receivers[i],None)) is not None:
                senders[(i+1)%len(phase)](n)
                ans = n
            else:
                return ans



print(f"part 1: {max((run_seq(phase) for phase in permutations(range(5))))}")
print(f"part 2: {max((run_seq2(phase) for phase in permutations(range(5,10))))}")
