from problem import gpl

pl = [[int(line[c:c+5]) for c in range(0,15,5)] for line in gpl()]

p2 = 0
for i in range(0,len(pl), 3):
    for j in range(3):
        abc = [pl[i][j], pl[i+1][j], pl[i+2][j]]
        abc.sort()
        a, b, c = abc
        p2 += a + b > c

p1 = 0
for abc in pl:
    abc.sort()
    a, b, c = abc
    p1 += a + b > c
    # is b + c > a? yes, c >= a.

print(f"part 1: {p1}")
print(f"part 2: {p2}")
