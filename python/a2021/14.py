from common import get_problem

# input = get_problem(2021, 14)

input = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

input = input.split('\n')

start = list(input[0])

splits = dict()

for line in input[1:]:
    if not line.strip():
        continue
    (l,r) = line.split(' -> ')
    splits[(l[0],l[1])] = [l[0], r]


chars = {chr(i) for i in range(ord('A'),ord('Z')+1)}
encodings = dict() # (a,b) -> 12
rencodings = dict() # 12 -> [a,b]

for c in chars:
    rencodings[c] = [c]

current = 0

def encode(l):
    global encodings, current
    l_ = list()
    i = 0
    while i + 1 < len(l):
        if (l[i],l[i+1]) not in encodings:
            encodings[(l[i], l[i+1])] = current
            rencodings[current] = [l[i],l[i+1]]
            current += 1
        l_.append(encodings[(l[i],l[i+1])])
        i += 2
    if i < len(l):
        l_.append(l[-1])
    return(l_)

def split(l, r):
    global splits
    if (l, r) in splits:
        return splits[(l,r)]
    l_ = split_list(rencodings[l] + [rencodings[r][0]])
    while l_[-1] not in chars:
        l_ = l_[:-1] + rencodings[l_[-1]]
    l_ = l_[:-1]
    while len(l_) > 3:
        l_ = encode(l_)
    splits[(l,r)] = l_
    return l_

def split_list(l):
    l_ = list()
    for i in range(len(l)-1):
        l_ += split(l[i],l[i+1])
    l_.append(l[-1])
    return l_

def expand(l):
    while not all(x in chars for x in l):
        l_ = list()
        for x in l:
            l_ += rencodings[x]
        l = l_
    return l

print(start)
for n in range(100):
    start = split_list(start)
    start = encode(start)

    #print(start)
    #for c in expand(start): print(c, end='')
    #print()
    print(n, len(start), max([i for i in start if i not in chars]))
