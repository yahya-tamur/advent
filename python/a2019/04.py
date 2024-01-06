from common import gp
l, r = gp().strip().split('-')
l, r = int(l), int(r)

p1, p2 = 0, 0
for i in range(l,r+1):
    pairs = list(zip(str(i)[:-1], str(i)[1:]))
    if all((i <= j for i, j in pairs)):
        p1 += not all((i < j for i, j in pairs))
        s = '-' + str(i) + '-'
        p2 += any((i != j and j == k and k != l for i,j,k,l in \
                zip(s[:-3], s[1:-2], s[2:-1], s[3:])))

print(f"part 1: {p1}")
print(f"part 2: {p2}")

