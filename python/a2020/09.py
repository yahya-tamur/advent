from common import gpl
from collections import deque
from sys import exit

lines = [int(i) for i in gpl()]

n = 25

avai = deque([x + y for i, x in enumerate(lines[:n]) \
        for j, y in enumerate(lines[:n]) if i != j])

invalid = 0
for i in range(n,len(lines)):
    z = lines[i]
    if z not in avai:
        invalid = z
        break
    for y in lines[i-n+1:i]:
        avai.append(y+z)
        avai.popleft()

print(f"part 1: {invalid}")

for i in range(len(lines)-1):
    acc = lines[i]
    for j in range(i+1,len(lines)):
        acc += lines[j]
        if acc > invalid:
            break
        if acc == invalid:
            print(f"part 2: {min(lines[i:j+1]) + max(lines[i:j+1])}")
            exit()



