from intcode import execute, interact, get_code

code = get_code()

out = execute(code.copy(), [])

print(f"part 1: {sum((out[i] == 2 for i in range(2,len(out),3)))}")

code[0] = 2
init, sendrecv = interact(code)

map = dict()

def um(out):
    global map
    for i in  range(0,len(out),3):
        map[(out[i],out[i+1])] = out[i+2]

um(init)

while any((i == 2 for i in map.values())):
    # inefficient.
    ball = next((i for i in map if map[i] == 4))
    paddle = next((i for i in map if map[i] == 3))
    if ball[0] > paddle[0]:
        um(sendrecv(1))
    elif ball[0] < paddle[0]:
        um(sendrecv(-1))
    else:
        um(sendrecv(0))

print(f"part 2: {map[(-1,0)]}")
