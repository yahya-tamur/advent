from problem import gp

inp = gp().strip()

p1, i = 0, 0
while (l := inp.find('(', i)) != -1:
    r = inp.find(')', i)
    m, n = (int(x) for x in inp[l+1:r].split('x'))
    p1 += l - i + m*n
    i = r+1+m

p1 += len(inp) - i

print(f"part 1: {p1}")

# You can have complicated patterns:
# Y combinator: (5x2)(5x2)AA or (6x2)B(6x2)AA
# This solution assumes that:
# (.x.)__(,x,)_______ if __ is the scope or (.x.),
# the scope of (,x,) doesn't extend past it.
# But it is linear!

multipliers = list()
multiplier = 1

p2, i = 0, 0
while i < len(inp):
    while multipliers and multipliers[-1][0] <= i:
        multiplier //= multipliers.pop()[1]
    if inp[i] == '(':
        r = inp.find(')', i)
        m, n = (int(x) for x in inp[i+1:r].split('x'))
        multipliers.append((r+1+m,n))
        multiplier *= n
        i = r+1
    else:
        p2 += multiplier
        i += 1

print(f"part 2: {p2}")
