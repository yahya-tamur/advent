from common import gpl

# 🌟🌟🌟
# Concise parser-free implementation.
# The way the precedence is done in part 2 is similar to the way you would
# implement precedence with a parser.

def get_seq1(s):
    spaces = [i for i in range(len(s)) if s[i] == ' ']
    if len(spaces) < 3:
        return eval(s)
    return get_seq1(str(eval(s[:spaces[2]])) + s[spaces[2]:])

def get_seq2(s):
    if s.find('*') == -1:
        return eval(s)
    l, _, r = s.partition('*')
    return get_seq2(l)*get_seq2(r)

get_seq = [get_seq1, get_seq2]

def get_ans(s, part):
    if s.find('(') == -1:
        return get_seq[part](s)
    r = s.find(')')
    l = s.rfind('(',0,r)
    return get_ans(s[:l] + str(get_seq[part](s[l+1:r])) + s[r+1:], part)


print(f"part 1: {sum((get_ans(l, 0) for l in gpl()))}")
print(f"part 2: {sum((get_ans(l, 1) for l in gpl()))}")
