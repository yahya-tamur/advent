from problem import gpl

inp = list()

for line in gpl():
    words = line.split(' ')
    inp.append((int(words[3]), int(words[-1][:-1])))

def solve(inp):
    cycle = 1
    time = 0

    for i, (m, d) in enumerate(inp):
        for new_time in range(time, cycle*m + time, cycle):
            if (new_time + i + 1 + d) % m == 0:
                time = new_time
                break
        cycle *= m

    return time

print(f"part 1: {solve(inp)}")

inp.append((11, 0))

print(f"part 2: {solve(inp)}")
