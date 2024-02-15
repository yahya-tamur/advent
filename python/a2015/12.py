from problem import gp

inp = gp().strip()

def addnums(inp):
    ans = 0
    i = 0

    while True:

        while i < len(inp) and not inp[i].isnumeric():
            i += 1

        if i == len(inp):
            break
        j = i + 1
        while j < len(inp) and inp[j].isnumeric():
            j += 1

        a = int(inp[i:j])
        if i > 0 and inp[i-1] == '-':
            a = -a
        ans += a

        i = j

    return ans

print(f"part 1: {addnums(inp)}")

delete_this = []

lastsep_i = []
lastsep_red = []

j = len(inp)-1

while j >= 0:
    if inp[j] in '[{':
        i = lastsep_i.pop()
        red = lastsep_red.pop()
        if red:
            delete_this.append((j, i+1))
    elif inp[j] in ']}':
        lastsep_i.append(j)
        lastsep_red.append(False)
    next_j = [x for x in [inp.rfind(c,0,j) for c in '[{}]'] if x >= 0]
    if not next_j:
        break
    j_ = max(next_j)

    if lastsep_i and inp[lastsep_i[-1]] == '}' and '"red"' in inp[j_:j]:
        lastsep_red[-1] = True

    j = j_

delete_this.sort(key=lambda t: t[1])

last_deleted = len(inp) + 10

for (i,j) in delete_this[::-1]:
    if j > last_deleted:
        continue
    inp = inp[:i] + inp[j:]
    last_deleted = i


print(f"part 2: {addnums(inp)}")
