# Takes about 30s.

from problem import gpl

a, b = [int(s.split(' ')[-1]) for s in gpl()]

p1 = 0
for i in range(40_000_000):
    a = a*16807 % 2147483647
    b = b*48271 % 2147483647
    p1 += a & ((1 << 16) - 1) == b & ((1 << 16) - 1)

print(f"part 1: {p1}")

a, b = [int(s.split(' ')[-1]) for s in gpl()]

p2 = 0
for i in range(5_000_000):
    a = a*16807 % 2147483647
    while a & 3 != 0:
        a = a*16807 % 2147483647
    b = b*48271 % 2147483647
    while b & 7 != 0:
        b = b*48271 % 2147483647

    p2 += a & ((1 << 16) - 1) == b & ((1 << 16) - 1)

print(f"part 2: {p2}")
