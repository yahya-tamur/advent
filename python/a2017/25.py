from problem import gp
from collections import defaultdict

blocks = gp().split('\n\n')

#(State x current value) |-> (value, tape step, new state)
delta = dict()

for block in blocks[1:]:
    in_state, _, v0, d0, s0, _, v1, d1, s1, *_ = block.split('\n')
    state = in_state[-2]
    v0, v1 = int(v0[-2]), int(v1[-2])
    d0, d1 = 1 if 'right' in d0 else -1, 1 if 'right' in d1 else -1
    s0, s1 = s0[-2], s1[-2]
    delta[(state, 0)] = (v0, d0, s0)
    delta[(state, 1)] = (v1, d1, s1)

init = blocks[0].split('\n')

state = init[0][-2]
steps = int(init[1].split(' ')[-2])

loc = 0
tape = defaultdict(int)

for _ in range(steps):
    value, tape_step, state = delta[(state, tape[loc])]
    tape[loc] = value
    loc += tape_step

print(f"part 1: {sum(tape.values())}")
print(f"part 2: {0}")

