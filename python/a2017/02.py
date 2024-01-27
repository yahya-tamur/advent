from problem import gpl

p1, p2 = 0, 0
for line in gpl():
    line = [int(i) for i in line.split('\t')]
    for i in line:
        for j in line:
            if i % j == 0 and j != 1 and i != j:
                p2 += i // j
    p1 += max(line) - min(line)

print(f"part 1: {p1}")
print(f"part 2: {p2}")

