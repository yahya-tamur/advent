from problem import gp

input = gp().strip()
n, m = 6, 25
print(len(input))
layers = [input[i:i+n*m] for i in range(0,len(input),n*m)]

minlayer = min(((layer.count('0'), layer) for layer in layers))[1]
print(f"part 1: {minlayer.count('1')*minlayer.count('2')}")

image = list()
for i in range(25*6):
    k = '2'
    for layer in layers:
        k = layer[i]
        if k != '2':
            break
    image.append(k)

print("part 2:")
for i in range(n):
    print(''.join((('#' if c == '1' else ' ') for c in image[i*m:(i+1)*m])))
