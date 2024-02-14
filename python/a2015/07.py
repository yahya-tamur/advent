from problem import gpl

d = dict()

for line in gpl():
    src, dst = line.split(' -> ')
    d[dst] = src

seen = {'NOT': -1, 'AND': -1, 'OR': -1, 'LSHIFT': -1, 'RSHIFT': -1}

def calc(s):
    if s in seen:
        return

    if ' ' not in s and not s.isalpha():
        seen[s] = int(s)
        return

    words = d[s].split(' ')

    for word in words:
        if word not in seen:
            calc(word)

    if len(words) == 1:
        seen[s] = seen[words[0]]
        return

    if len(words) == 2:
        seen[s] = ~seen[words[1]]
        return

    l, op, r = words

    match op:
        case 'AND':
            seen[s] = seen[l] & seen[r]
        case 'OR':
            seen[s] = seen[l] | seen[r]
        case 'LSHIFT':
            seen[s] = seen[l] << seen[r]
        case 'RSHIFT':
            seen[s] = seen[l] >> seen[r]

calc('a')
p1 = seen['a']

print(f"part 1: {p1}")

seen = {'NOT': -1, 'AND': -1, 'OR': -1, 'LSHIFT': -1, 'RSHIFT': -1, 'b': p1}

calc('a')

print(f"part 2: {seen['a']}")
