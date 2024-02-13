# This was hard to decode, and fun solution!
# Bit tired after doing this right after 23 though.
# That was hard too. I was pretty scared of the tgl instruction!

from problem import gpl

mn = int(gpl()[1].split(' ')[1])*int(gpl()[2].split(' ')[1])

s = 2
while s <= mn:
    s = 4*s + 2

print(f"part 1: {s - mn}")
print(f"part 2: {0}")
