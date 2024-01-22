from problem import gpl
from collections import deque, defaultdict

inp = gpl()

def run(elfpower):
    m = defaultdict(lambda:'#')
    for i, line in enumerate(inp):
        for j, c in enumerate(line):
            m[i+1j*j] = c
    units = [(loc, c, 200) for loc, c in m.items() if c in 'GE']

    def rc(z):
        return (int(z.real), int(z.imag))

    op = {'G': 'E', 'E': 'G'}
    atk = {'E': elfpower, 'G': 3}

    finished = False
    for _n in range(5000):
        units.sort(key=lambda u: rc(u[0]))
        for ui, (loc, typ, hp) in enumerate(units):
            if hp <= 0:
                continue
            if all((u[1] == typ or u[2] <= 0 for u in units)):
                finished = True
                break

            if not any((m[loc + d] == op[typ] for d in [1,-1,1j,-1j])):
                targets = {u[0] + d for u in units if u[1] != typ and u[2] > 0 \
                        for d in [1,-1,1j,-1j] if m[u[0]+d] == '.'}

                wavefront = [(loc + d, {loc + d}) for d in [1,-1,1j,-1j] if m[loc+d] == '.']
                seen = {loc}
                found = set()

                while wavefront and not found:
                    wavefront_ = list()

                    for (wloc, starts) in wavefront:
                        if wloc in targets:
                            found |= starts
                            continue
                        if wloc in seen:
                            continue
                        seen.add(wloc)

                        for d in [1,-1,1j,-1j]:
                            if m[wloc + d] != '.':
                                continue
                            newloc = True
                            for i, (wloc_, starts_) in enumerate(wavefront_):
                                if wloc + d == wloc_:
                                    wavefront_[i] = (wloc_, starts | starts_)
                                    newloc = False
                            if not newloc:
                                continue
                            wavefront_.append((wloc+d, starts))
                    wavefront = wavefront_

                if found:
                    new_loc = min(found, key=rc)
                    m[loc] = '.'
                    m[new_loc] = typ
                    units[ui] = (new_loc, typ, hp)
                    loc = new_loc

            targets = [i for i, u in enumerate(units) if abs(u[0] - loc) == 1 and u[1] == op[typ] and u[2] > 0]
            if not targets:
                continue
            target = min(targets, key=lambda i: (units[i][2], rc(units[i][0])))
            loc_, typ_, hp_ = units[target]
            units[target] = (loc_, typ_, hp_ - atk[typ])
            if hp_ - atk[typ] <= 0:
                m[loc_] = '.'

        for i in range(len(units)-1,-1,-1):
            loc, typ, hp = units[i]
            if hp <= 0:
                if typ == 'E' and elfpower > 3:
                    return None
                units.pop(i)

        if finished:
            return _n*sum((u[2] for u in units))

print(f"part 1: {run(3)}")
k, p2 = 4, None
while (p2 := run(k)) is None:
    k += 1
print(f"part 2: {p2}")

