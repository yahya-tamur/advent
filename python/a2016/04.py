from problem import gpl
from collections import defaultdict

p1 = 0
p2 = None
for line in gpl():
    occ = defaultdict(int)
    for c in line[:line.rfind('-')]:
        if c != '-':
            occ[c] += 1
    occ = [(-n, c) for c, n in occ.items()]
    occ.sort()
    enc = ''.join((occ[i][1] for i in range(5)))

    sid = int(line[line.rfind('-')+1:line.find('[')])
    if enc == line[-6:-1]:
        p1 += sid
        if p2 is None:
            dec = ''
            for c in line[:line.rfind('-')]:
                if c == '-':
                    dec += ' '
                else:
                    dec += chr( (ord(c)-ord('a') + sid) % 26 + ord('a') )
            if 'north' in dec:
                p2 = sid
        

print(f"part 1: {p1}")
print(f"part 2: {p2}")
