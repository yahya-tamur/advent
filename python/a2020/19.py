from common import gp

# 🌟🌟🌟
# I thought about this a little bit and came up with this very simple solution.
# I'm not sure if it's actually efficient but runs on 0.2s real and 0.004s sys,
# on par with rust solution on reddit. Maybe it would be less efficient with
# more recursive grammars?

# get_rule(s, i, <rule num>) returns set of numbers j such that s[i:j] matches
# the rule.
# get_rule_seq returns the same, but takes the input "<rule> <rule> ..."

rules = dict()
for line in gp().split('\n\n')[0].split('\n'):
    l, _, r = line.partition(': ')
    rules[int(l)] = r

def get_rule_seq(s, i, rule):
    ans = {i}
    for r in rule.split(' '):
        ans_ = set()
        for j in ans:
            ans_ |= get_rule(s, j, r)
        ans = ans_
    return ans

def get_rule(s, i, num):
    rule = rules[int(num)]

    if '"' in rule:
        if i < len(s) and s[i] == rule[1]:
            return {i+1}
        else:
            return set()
    if '|' in rule:
        l, _, r = rule.partition(' | ')
        return get_rule_seq(s, i, l) | get_rule_seq(s, i, r)

    return get_rule_seq(s, i, rule)

def get_ans():
    return sum((len(m) in get_rule(m,0,0) \
            for m in gp().split('\n\n')[1].split('\n')))

print(f"part 1: {get_ans()}")

rules[8] = '42 | 42 8'
rules[11] = '42 31 | 42 11 31'

print(f"part 2: {get_ans()}")
