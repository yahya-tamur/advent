from problem import gpl

g = [list(line) for line in gpl()]

carts = list()
g_ = dict()
for i, line in enumerate(g):
    for j, c in enumerate(line):
        g_[i+1j*j] = c
        if (d := {'^':-1, '>':1j, '<':-1j, 'v':1}.get(c)) is not None:
            carts.append((i, j, d, 0))
g_[-10-10j] = '|'
g = g_

first_crash = False

while True:
    carts.sort()
    to_remove = set()
    for k, (i, j, d, c) in enumerate(carts):
        z = (i + 1j*j) + d
        match g[z]:
            case '/':
                d = -1j/d
            case '\\':
                d = 1j/d
            case '+':
                match c:
                    case 0:
                        d *= 1j
                    case 2:
                        d *= -1j
                c = (c+1) % 3
        for k_, (i_, j_, _, _) in enumerate(carts):
            if (i_, j_) == (z.real, z.imag):
                if not first_crash:
                    print(f"part 1: {f'{int(j_)},{int(i_)}'}")
                    first_crash = True
                to_remove.add(k)
                to_remove.add(k_)
                #avoid further crashes
                carts[k_] = (-10, -10, 0, 0)
                z = -10-10j
                break
        carts[k] = (z.real, z.imag, d, c)
    for k in sorted(to_remove, reverse=True):
        carts.pop(k)
    if len(carts) == 1:
        print(f"part 2: {f'{int(carts[0][1])},{int(carts[0][0])}'}")
        break
