from problem import gpl

p1 = sum(
        (sum(c in 'aeiou' for c in line) >= 3) and \
        any(line[i] == line[i+1] for i in range(len(line)-1)) and \
        all(s not in line for s in ('ab', 'cd', 'pq', 'xy')) \
        for line in gpl())

print(f"part 1: {p1}")

p2 = sum(
        any(line[i:i+2] in line[i+2:] for i in range(len(line)-3)) and \
        any(line[i] == line[i+2] for i in range(len(line)-2))
        for line in gpl())

print(f"part 2: {p2}")
