from problem import gpl

sue = { \
    "children": 3, \
    "cats": 7, \
    "samoyeds": 2, \
    "pomeranians": 3, \
    "akitas": 0, \
    "vizslas": 0, \
    "goldfish": 5, \
    "trees": 3, \
    "cars": 2, \
    "perfumes": 1, \
}

gt = {'cats', 'trees'}
lt = {'pomeranians', 'goldfish'}
eq = {n for n in sue if n not in gt and n not in lt}

for i, line in enumerate(gpl()):
    line = line[line.find(':')+2:]
    phrases = [phrase.split(': ') for phrase in line.split(', ')]
    phrases = [(l, int(r)) for (l, r) in phrases]
    if all(sue[l] == r for (l, r) in phrases):
        print(f"part 1: {i+1}")
    if all( (l in gt and r > sue[l]) or \
            (l in lt and r < sue[l]) or \
            (l in eq and r == sue[l]) \
            for (l, r) in phrases):
        print(f"part 2: {i+1}")
