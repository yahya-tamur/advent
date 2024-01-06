# generator -> generator
def run(code, inp):
    def get(i):
        match (code[pc] // (10 ** (i+1))) % 10:
            case 0:
                return code[code[pc+i]]
            case 1:
                return code[pc+i]
            case n:
                print('lma')
    def out(i):
        return code[pc+i]
    input_index = 0
    pc = 0
    while True:
        match code[pc] % 100:
            case 1:
                code[out(3)] = get(1) + get(2)
                pc += 4
            case 2:
                code[out(3)] = get(1) * get(2)
                pc += 4
            case 3:
                code[out(1)] = next(inp)
                pc += 2
            case 4:
                yield get(1)
                pc += 2
            case 5:
                pc = get(2) if get(1) else pc + 3
            case 6:
                pc = get(2) if not get(1) else pc + 3
            case 7:
                code[out(3)] = get(1) < get(2)
                pc += 4
            case 8:
                code[out(3)] = get(1) == get(2)
                pc += 4
            case 99:
                break
            case x:
                print("asd", x)

#list -> list
def execute(code, inp):
    return list(run(code, iter(inp)))

#() -> send, recv
def interact(code):
    from collections import deque
    channel = deque()

    def send(i):
        channel.append(i)

    def recv():
        while True:
            yield channel.popleft()

    return send, run(code, recv())
