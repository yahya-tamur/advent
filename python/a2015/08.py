from problem import gpl

p1 = 0
hexchars = '0123456789abcdef'

for line in gpl():
    if len(line) >= 2 and line[0] == '"' and line[-1] == '"':
        p1 += 2
        line = line[1:-1]
    i = 0
    while i < len(line):
        if i < len(line) - 1 and line[i:i+2] == '\\\"' or line[i:i+2] == '\\\\':
            i += 2
            p1 += 1
            continue
        if i + 3 < len(line) and line[i:i+2] == '\\x' and line[i+2] in hexchars \
                and line[i+3] in hexchars:
            i += 4
            p1 += 3
            continue
        i += 1

print(f"part 1: {p1}")

p2 = sum(line.count('\\') + line.count('\"') + 2 for line in gpl())

print(f"part 2: {p2}")
