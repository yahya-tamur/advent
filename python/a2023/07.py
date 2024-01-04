from common import get_problem_lines
from collections import defaultdict


def part2_score(hand):
    scores = {c: i for (i, c) in enumerate('J23456789TQKA')}
    hscore = 0
    for c in hand:
        hscore = hscore*20 + scores[c]
    
    grps = defaultdict(int)
    for c in hand:
        grps[c] += 1
    j = 0
    if 'J' in grps:
        j = grps.pop('J')
    l = list(grps.values())
    l.sort(key = lambda i:-i)
    if not l:
        l = [5]
    else:
        l[0] += j
    return (l, hscore)

def part1_score(hand):
    scores = {c: i for (i, c) in enumerate('23456789TJQKA')}
    hscore = 0
    for c in hand:
        hscore = hscore*20 + scores[c]
    
    grps = defaultdict(int)
    for c in hand:
        grps[c] += 1
    l = list(grps.values())
    l.sort(key = lambda i:-i)
    return (l, hscore)

input = [line.split(' ') for line in get_problem_lines()]

def score(scorer):
    hands = [(scorer(l), int(r)) for (l,r) in input]

    hands.sort()
    ans = 0
    for (i, (_, r)) in enumerate(hands):
        ans += (i+1)*r
    return ans

print(f"part 1: {score(part1_score)}")
print(f"part 2: {score(part2_score)}")
                               
