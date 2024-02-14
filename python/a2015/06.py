from problem import gpl

lights = [0 for _ in range(1000)]

for line in gpl():
    words = line.split(' ')
    x, y = eval(words[-3])
    x_, y_ = eval(words[-1])

    mask = (1 << (x_+1)) - (1 << x)

    if words[0] == 'toggle':
        for i in range(y, y_+1):
            lights[i] ^= mask
    elif words[1] == 'on':
        for i in range(y, y_+1):
            lights[i] |= mask
    else:
        for i in range(y, y_+1):
            lights[i] &= ~mask

print(f"part 1: {sum(n.bit_count() for n in lights)}")


lights = [[0 for _ in range(1000)] for _ in range(1000)]

for line in gpl():
    words = line.split(' ')
    x, y = eval(words[-3])
    x_, y_ = eval(words[-1])

    mask = (1 << (x_+1)) - (1 << x)

    if words[0] == 'toggle':
        for j in range(x, x_+1):
            for i in range(y, y_+1):
                lights[i][j] += 2
    elif words[1] == 'on':
        for j in range(x, x_+1):
            for i in range(y, y_+1):
                lights[i][j] += 1
    else:
        for j in range(x, x_+1):
            for i in range(y, y_+1):
                lights[i][j] = max(0, lights[i][j]-1)

print(f"part 2: {sum(sum(n) for n in lights)}")
