from problem import gpl

part1 = 0

empty = {code for code in range(128*8)}

for code in gpl():
    code = code \
        .replace("F", "0") \
        .replace("B", "1") \
        .replace("L","0") \
        .replace("R","1")

    code = int(code, base=2)
    part1 = max(part1, code)

    empty.remove(code)

print(f"part 1: {part1}")

for code in empty:
    if code - 1 not in empty and code + 1 not in empty:
        print(f"part 2: {code}")
