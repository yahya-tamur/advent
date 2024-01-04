from common import gpl

def evalpar(s):
    print(s)
    if s.find('(') == -1:
        return evalstraight(s)
    r = s.find(')')
    l = s.rfind('(',0,r)
    return evalpar(s[:l] + str(evalstraight(s[l+1:r])) + s[r+1:])

def evalstraight(s):
    s = s.split(' ')
    acc = int(s[0])
    for i in range(1,len(s),2):
        acc = eval(f"{acc}{s[i]}{s[i+1]}")
    return acc

def evalparplusfirst(s):
    print(s)
    if s.find('(') == -1:
        return evalstraightplusfirst(s)
    r = s.find(')')
    l = s.rfind('(',0,r)
    return evalparplusfirst(s[:l] + str(evalstraightplusfirst(s[l+1:r])) + s[r+1:])

def evalstraightplusfirst(s):
    if s.find('*') == -1:
        return eval(s)
    l, _, r = s.partition('*')
    return evalstraightplusfirst(l)*evalstraightplusfirst(r)

print(f"part 1: {sum((evalpar(l) for l in gpl()))}")
print(f"part 2: {sum((evalparplusfirst(l) for l in gpl()))}")
