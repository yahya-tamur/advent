# 🌟🌟🌟
# This was fun to figure out!

from problem import gp

num = int(gp())

l = list(range(1, num)) + [0]

i = 0

while l[i] != i:
    l[i] = l[l[i]]
    i = l[i]

print(f"part 1: {i + 1}")

#num = 5
l = list(range(1, num)) + [0]

ln, c = num, (num // 2) - 1

while l[c] != c:
    l[c] = l[l[c]]

    if ln % 2 == 1:
        c = l[c]

    ln -= 1

print(f"part 2: {c + 1}")
