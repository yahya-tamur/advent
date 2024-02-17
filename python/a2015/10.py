from problem import gp

l = [int(x) for x in gp().strip()]

def process(l):
    l_ = []
    repeat, c = 1, l[0]

    for c_ in l[1:]:
        if c == c_:
            repeat += 1
        else:
            for x in str(repeat):
                l_.append(int(x))
            l_.append(c)
            repeat, c = 1, c_
    for x in str(repeat):
        l_.append(int(x))
    l_.append(c)
    return l_

for _ in range(40):
    l = process(l)

print(f"part 1: {len(l)}")

for _ in range(10):
    l = process(l)

print(f"part 2: {len(l)}")
