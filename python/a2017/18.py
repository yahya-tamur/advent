from problem import gpl
from collections import defaultdict, deque

inss = [line.split(' ') for line in gpl()]

def program(p, send, recv):
    v = defaultdict(int)
    for line in inss:
        for word in line:
            if not word.isalpha():
                v[word] = int(word)
    v['p'] = p

    ip = 0
    num_sends = 0

    while True:
        # Actually, the program never terminates, and that helps simplify this.
        ins, r1 = inss[ip][:2]
        r2 = None if len(inss[ip]) == 2 else inss[ip][2]
        match ins:
            case 'snd':
                send.append(v[r1])
                num_sends += 1
            case 'set':
                v[r1] = v[r2]
            case 'add':
                v[r1] += v[r2]
            case 'mul':
                v[r1] *= v[r2]
            case 'mod':
                v[r1] %= v[r2]
            case 'rcv':
                while len(recv) == 0:
                    yield num_sends
                v[r1] = recv.popleft()
            case 'jgz':
                if v[r1] > 0:
                    ip += v[r2]
                    continue
        ip += 1

p0in, p1in = deque([]), deque([])
p0, p1 = program(0, p1in, p0in), program(1, p0in, p1in)

c0 = next(p0)
print(f"part 1: {p1in[-1]}")
c1 = next(p1)

while p0in or p1in:
    c0 = next(p0)
    c1 = next(p1)

print(f"part 2: {c1}")



