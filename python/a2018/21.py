# I tried to change to code a bit and actually run it, but my interpreter
# was way too slow. I already had decompiled the program this much.
# This should work as long the only things that change between different
# users is this number 'a'. Only two lines!

from problem import gpl

a, r, seen = int(gpl()[8].split(' ')[1]), 0, list()

while (r := ( (a + (r & 255))*65899*65899*65899 + \
            ((r >> 8) & 255)*65899*65899 + \
            ((1 | (r >> 16)) & 255)*65899 ) & ( (2 ** 24) - 1 ) ) \
       not in seen: seen.append(r)

print(f"part 1: {seen[0]}")
print(f"part 2: {seen[-1]}")
