from problem import gp
from intcode import execute, interact

code = [int(i) for i in gp().strip().split(',')]

out = execute(code.copy(), [])

print(f"part 1: {sum((out[i] == 2 for i in range(2,len(out),3)))}")


outlen = len(out)
code[0] = 2
send, recv = interact(code)

send(0)
send(0)
send(0)
send(1)
for i in range(10):
    send(1)

    print(f"i: {i}")
    out = list()
    while (x := next(recv)) != "wait":
        out.append(x)

    print(len(out))
    map = dict()
    for i in  range(0,len(out),3):
        map[(out[i],out[i+1])] = out[i+2]
        #print(out[i], out[i+1], out[i+2])

    #print((-1,0) in map)
#code[2
    if map:
        xl = max((x for x, _ in map))
        yl = max((y for _, y in map))
        print('as', xl, yl)
#.
        for y in range(22):
            for x in range(41):
                if (x,y) in map:
                    print(map[(x,y)], end='')
                else:
                    print(' ', end='')
            print()
        for x in range(41):
            print(x%10,end='')
        print()

