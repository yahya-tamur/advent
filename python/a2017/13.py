from problem import gpl

layers = list()

for line in gpl():
    l, r = line.split(': ')
    l, r = int(l), int(r)
    while l >= len(layers):
        layers.append(0)
    layers[l] = r

print(f"part 1: {sum(( (i % ((li-1)*2) == 0) and i*li for i, li in enumerate(layers)))}")

for s in range(99999999999):
    if all(( li == 0 or (i+s) % ((li-1)*2) for i, li in enumerate(layers))):
        print(f"part 2: {s}")
        break


