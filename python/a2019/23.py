from intcode import get_code, interact
from collections import deque

computers = list()
for i in range(50):
    init, sv = interact(get_code())
    # these were all empty!
    sv(i)
    computers.append(sv)

channels = [[] for _ in range(50)]
nat = None
pnat = None
p1posted = False
while True:
    for i in range(50):
        if not channels[i]:
            channels[i].append(-1)
        send = list()
        for j in channels[i]:
            send.extend(computers[i](j))
        channels[i] = list()
        for i in range(0, len(send), 3):
            (a, b, c) = send[i:i+3]
            if a == 255:
                if not p1posted:
                    print(f"part 1: {c}")
                    p1posted = True
                nat = (b,c)
            else:
                channels[a].extend([b,c])
    if all((len(l) == 0 for l in channels)):
        if pnat == nat:
            print(f"part 2: {pnat[1]}")
            break
        pnat = nat
        channels[0].extend(nat)



