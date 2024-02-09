from problem import gp
from md5 import fast_md5

inp = gp().strip()

def solve(rep):

    def calc(i):
        s = inp + str(i)
        for _ in range(rep):
            s = fast_md5(s)
        return s

    # loops once, not once per character
    def reps(s):
        r3, r5 = list(), list()
        current = s[0]
        count = 1
        for c in s[1:]:
            if c == current:
                count += 1
            else:
                current = c
                count = 1
            if count == 3 and len(r3) == 0:
                r3.append(c)
            if count == 5 and c not in r5:
                r5.append(c)
        return (r3, r5)

    loops = [reps(calc(i)) for i in range(1000)]

    i = 1
    found = 0

    while found < 64:
        r3 = loops[i%1000][0]
        loops[i%1000] = reps(calc(i+1000))


        for c in r3:
            if any(c in r5 for _, r5 in loops):
                print(i)
                found += 1
                break

        i += 1
    return i - 1

print(f"part 1: {solve(1)}")
print(f"part 2: {solve(2017)}")
