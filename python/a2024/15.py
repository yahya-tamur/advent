from problem import get_problem, get_problem_lines

m = dict()
loc = 0

pl = list(get_problem_lines())

B = next(i for i in range(len(pl)) if pl[i][0] != '#')

for i, line in enumerate(pl[:B]):
    for j, c in enumerate(line):
        m[i+1j*j] = c
        if c == '@':
            loc = i+1j*j

for ins in ''.join(pl[B:]):
    d = {'^':-1, 'v':1, '<':-1j, '>':1j}[ins]
    match m[loc+d]:
        case '.':
            m[loc+d] = '@'
            m[loc] = '.'
            loc += d
        case '#':
            pass
        case 'O':
            l = 1
            while m[loc+l*d] == 'O':
                l += 1
            if m[loc+l*d] == '.':
                m[loc+l*d] = 'O'
                m[loc+d] = '@'
                m[loc] = '.'
                loc += d


print(f"part 1: {sum(int(100*z.real + z.imag) for z, c in m.items() if c == 'O')}")



m = dict()
loc = 0

pl = list(get_problem_lines())

B = next(i for i in range(len(pl)) if pl[i][0] != '#')

for i, line in enumerate(pl[:B]):
    for j, c in enumerate(line):
        match c:
            case '.':
                m[i+2j*j] = '.'
                m[i+2j*j+1j] = '.'
            case 'O':
                m[i+2j*j] = '['
                m[i+2j*j+1j] = ']'
            case '#':
                m[i+2j*j] = '#'
                m[i+2j*j+1j] = '#'
            case '@':
                m[i+2j*j] = '@'
                m[i+2j*j+1j] = '.'
                loc = i+2j*j

for ins in ''.join(pl[B:]):
    d = {'^':-1, 'v':1, '<':-1j, '>':1j}[ins]
    match m[loc+d]:
        case '.':
            m[loc+d] = '@'
            m[loc] = '.'
            loc += d
        case '#':
            pass
        case _:
            can_move = True
            to_move = [loc]
            looking = [loc+d]
            looked = {loc}
            while looking:
                z = looking.pop()
                if z in looked:
                    continue
                looked.add(z)
                match m[z]:
                    case '.':
                        pass
                    case '#':
                        can_move = False
                        break
                    case _:
                        to_move.append(z)
                        looking.append(z+d)
                        if d in (-1,1):
                            looking.append(z+{'[': 1j, ']':-1j}[m[z]])
            if not can_move:
                continue
            to_move.sort(key=lambda z:(-z/d).real)
            for z in to_move:
                m[z+d] = m[z]
                m[z] = '.'
            loc += d



print(f"part 2: {sum(int(100*z.real + z.imag) for z, c in m.items() if c == '[')}")


