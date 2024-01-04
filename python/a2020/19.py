from common import gp

rules = dict()
for line in gp().split('\n\n')[0].split('\n'):
    l, _, r = line.partition(': ')
    rules[int(l)] = r

# There are better ways of doing this (actual parser, etc.) but this works here.

mem = dict()

def get_rule(num):
    if int(num) in mem:
        return mem[int(num)]
    rule = rules[int(num)]
    ans = "bla"
    if '"' in rule:
        ans = {rule[1]}
    elif len(rule.split(' ')) == 1:
        ans = get_rule(rule)
    elif '|' in rule:
        if len(rule.split(' ')) == 3:
            a, _, b = rule.split(' ')
            ans = get_rule(a) | get_rule(b)
        else:
            a, b, _, c, d = rule.split(' ')
            ans = {l + r for l in get_rule(a) for r in get_rule(b)} | \
                    {l + r for l in get_rule(c) for r in get_rule(d)}
    else:
        a, b = rule.split(' ')
        ans = {l + r for l in get_rule(a) for r in get_rule(b)}
    mem[int(num)] = ans
    return ans

accept = get_rule(0)

p1 = 0
for message in gp().split('\n\n')[1].split('\n'):
    if message in accept:
        p1 += 1

print(f"part 1: {p1}")



