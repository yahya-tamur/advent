from intcode import execute, interact, get_code
from itertools import permutations

code = get_code()

def run_seq(phase):
    val = 0
    for p in phase:
        val = execute(code.copy(), [p, val])[0]
    return val

def run_seq2(phase):
    senders, receivers = list(), list()
    channels = list()
    for i in phase:
        _, sendrecv = interact(code.copy())
        _ = sendrecv(i)
        channels.append(sendrecv)

    signal = 0
    while True:
        for i in range(5):
            if (resp := channels[i](signal)) is not None:
                signal = resp[0]
            else:
                return signal


print(f"part 1: {max((run_seq(phase) for phase in permutations(range(5))))}")
print(f"part 2: {max((run_seq2(phase) for phase in permutations(range(5,10))))}")
