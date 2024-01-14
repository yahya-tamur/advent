from intcode import get_code, interact, execute
from collections import defaultdict

# Pretty efficient!

code = get_code()

p1 = 0
for i in range(50):
    for j in range(50):
        p1 += execute(code.copy(), [i,j])[0]

print(f"part 1: {p1}")

# size of the largest square ending at (i,j)
# calculated with dynamic programming.
bsa = defaultdict(int)
bsa[(-1,-1)] = 0

# range of i scanned
l, r = -10, 10

for n in range(5000):
    start = True
    for i in range(l,r):
        j = n - i
        z = i + j*1j

        # if surrounded by zeroes, skip. ones, don't bother running the intcode.
        if n > 50 and bsa[z-1] == 0 and bsa[z-1j] == 0:
            continue
        if not (bsa[z-1] > 0 and bsa[z-1j] > 0):
            if execute(code.copy(), [i,j])[0] == 0:
                continue

        if start:
            l = i - 10
            start = False
        r = i + 10

        if bsa[z-1] == 0 or bsa[z-1j] == 0:
            bsa[z] = 1
        elif bsa[z-1] != bsa[z-1j]:
            bsa[z] = min(bsa[z-1],bsa[z-1j]) + 1
        else:
            k = bsa[z-1j]
            if bsa[z-k*(1+1j)] > 0:
                bsa[z] = k + 1
            else:
                bsa[z] = k

        if bsa[z] >= 100:
            i, j = i - 99, j - 99 # go to the top left
            print(f"part 2: {10000*i + j}")
            from sys import exit
            exit()



