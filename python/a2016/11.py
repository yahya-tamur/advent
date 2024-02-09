# Takes a few minutes to run

from collections import deque
from problem import gpl

def solve(part):
    floors = [[] for _ in range(4)]
    num_floors = 4

    objects = dict()
    for i, line in enumerate(gpl()):
        if i == 0 and part == 2:
            line += "An elerium generator. An elerium-compatible microchip. A dilithium generator. A dilithium-compatible microchip."
        words = line.split(' ')
        for j in range(len(words)):
            if 'generator' in words[j]:
                w = words[j-1]
                if w not in objects:
                    objects[w] = len(objects)
                floors[i].append((objects[w], 1))

            if 'microchip' in words[j]:
                w = words[j-1].split('-')[0]
                if w not in objects:
                    objects[w] = len(objects)
                floors[i].append((objects[w], 0))

    num_items = len(objects)

    floors_ = list()
    for floor in floors:
        floors_.append(0)
        for (j, typ) in floor:
            floors_[-1] |= 1 << (j + typ*num_items)

    init = (0, tuple(floors_))


    def valid(state):
        e, floors = state
        for floor in floors:
            g, m = (floor >> num_items), (floor & ((1 << num_items) - 1))
            if g != 0 and (m & ~g) != 0:
                return False
        return True

    seen = set()
    active = deque([(0, init)])

    while active:
        steps, state = active.popleft()

        if state in seen:
            continue
        seen.add(state)

        e, floors = state

        if floors[-1] == (1 << 2*num_items) - 1:
            return(steps)

        for e_ in [x for x in (e+1, e-1) if x in range(num_floors)]:

            if all(floors[i] == 0 for i in range(e_+1)):
                continue

            for i in [i for i in range(2*num_items) if (1 << i) & floors[e]]:

                floors_ = list(floors)

                floors_[e_] |= 1 << i
                floors_[e] &= ~(1 << i)

                state_ = (e_, tuple(floors_))

                if state_ not in seen and valid(state_):
                    active.append((steps + 1, state_))

            for i in [i for i in range(1,2*num_items) if (1 << i) & floors[e]]:
                for j in [j for j in range(i) if (1 << j) & floors[e]]:

                    floors_ = list(floors)

                    floors_[e_] |= (1 << i) | (1 << j)
                    floors_[e] &= ~((1 << i) | (1 << j))

                    state_ = (e_, tuple(floors_))

                    if state_ not in seen and valid(state_):
                        active.append((steps + 1, state_))

print(f"part 1: {solve(1)}")
print(f"part 2: {solve(2)}")
