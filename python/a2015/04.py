from problem import gp
from md5 import fast_md5

p = gp().strip()

i = 1

while fast_md5(p + str(i))[:5] != '00000':
    i += 1

print(f"part 1: {i}")

while fast_md5(p + str(i))[:6] != '000000':
    i += 1

print(f"part 2: {i}")
