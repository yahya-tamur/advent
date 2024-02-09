from problem import gpl

def abba(s):
    for i in range(len(s)-3):
        if s[i] == s[i+3] and s[i+1] == s[i+2] and s[i] != s[i+2]:
            return True
    return False

def aba(s):
    ans = []
    for i in range(len(s)-2):
        if s[i] == s[i+2] and s[i] != s[i+1]:
            ans.append((s[i],s[i+1]))
    return ans

p1 = 0
p2 = 0
for line in gpl():
    ins, out = [], []
    i = 0
    while (k := line.find('[', i)) != -1:
        ins.append(line[i:k])
        i = line.find(']',i)
        out.append(line[k+1:i])
        i += 1
    ins.append(line[i:])
    ins, out = '&-*'.join(ins), '&-*'.join(out)
    p1 += abba(ins) and not abba(out)
    p2 += bool({(b,a) for (a,b) in aba(ins)} & set(aba(out)))

print(f"part 1: {p1}")
print(f"part 2: {p2}")
