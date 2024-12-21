from problem import get_problem, get_problem_lines, look

def man(z_, z):
    return abs(z_.real - z.real) + abs(z_.imag - z.imag)

def make_pad(pad):
    pad_ = dict()
    for i, line in enumerate(pad.split(',')):
        for j, c in enumerate(line):
            if c != '_':
                pad_[c] = i+1j*j
    return pad_

numpad = make_pad("789,456,123,_0A")
dirpad = make_pad("_^A,<v>")

# shortest path between two buttons
def shortest(start, end, pad):
    stack = [(start, [])]
    paths = []
    while stack:
        z, p = stack.pop()
        if z == end:
            paths.append(p)
            continue
        for d in (1, -1, 1j, -1j):
            z_ = z + d
            if man(z_, end) >= man(z, end) or z_ not in pad.values():
                continue
            stack.append((z_, p + [d]))

    return [''.join({1: 'v', -1: '^', 1j: '>', -1j: '<'}[d] for d in path) \
            for path in paths]

# get all shortest sequences of inputs to type the sequence
def unpad(seq, pad):
    seq = 'A' + seq
    paths = ['']
    for i in range(len(seq)-1):
        paths_ = []
        for p in paths:
            for s in shortest(pad[seq[i]], pad[seq[i+1]], pad):
                paths_.append(p + s + 'A')

        paths = paths_
    return paths

# get sequence of possible input sequnces. Return all possible sequences of the
# shortest length to type any one of them.
def shortest_unpad(seqs, pad):
    def lenseq(seq):
        return sum(man(pad[seq[i]], pad[seq[i+1]]) for i in range(len(seq)-1))

    ml = 9999*len(seqs[0])
    mls = []
    for ch, seq in seqs:
        if (s := lenseq(seq)) < ml:
            mls = [(ch, seq)]
            ml = s
        elif s == ml:
            mls.append((ch, seq))


    ans = []
    for ch, seq in mls:
        ans += [(ch, x) for x in unpad(seq, pad)]

    return ans

bests = dict()

for d1 in '^<>vA':
    for d2 in '^<>vA':
        r = [(x, x) for x in shortest(dirpad[d1], dirpad[d2], dirpad)]
        while len(set(x for x, _ in r)) != 1:
            r = shortest_unpad(r, dirpad)
        bests[(d1, d2)] = r[0][0]

from collections import Counter

def best_shortest(s):
    d, first = s
    d_ = Counter()
    start = bests[('A', first)] + 'A'
    first_ = start[0]
    d[('A', first)] += 1
    d_[('A', first_)] -= 1
    for (c1, c2), n in d.items():
        path = 'A' + bests[(c1, c2)] + 'A'
        for i in range(len(path) - 1):
            d_[(path[i], path[i+1])] += n

    return (d_, first_)

def into_counter(s):
    d = Counter()
    for i in range(len(s)-1):
        d[(s[i], s[i+1])] += 1
    return (d, s[0])

def solve(line, n):
    r = [into_counter(cs) for cs in unpad(line, numpad)]
    for _ in range(n):
        r = [best_shortest(x) for x in r]

    return min(sum(x[0].values()) + 1 for x in r)


ans, ans2 = 0, 0
for line in get_problem_lines():
    num = int(line[:3])
    ans += int(num*solve(line, 2))
    ans2 += int(num*solve(line, 25))

print(f"part 1: {ans}")
print(f"part 2: {ans2}")

