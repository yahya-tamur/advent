# generator -> generator
def run(code, inp):
    # do we need to switch to a hashmap instead?
    def extend_to(i):
        if (ext := i - len(code) + 1) > 0:
            code.extend([0]*ext)
    def get(i):
        match (code[pc] // (10 ** (i+1))) % 10:
            case 0:
                extend_to(code[pc+i])
                return code[code[pc+i]]
            case 1:
                return code[pc+i]
            case 2:
                extend_to(code[pc+i]+rb)
                return code[code[pc+i]+rb]
            case n:
                print(f'mode {n}')
    def out(i):
        match (code[pc] // (10 ** (i+1))) % 10:
            case 0:
                ans = code[pc+i]
            case 2:
                ans = code[pc+i]+rb
            case n:
                print(f'mode {n}')
        extend_to(ans)
        return ans
    input_index = 0
    pc = 0
    rb = 0
    while True:
        extend_to(pc+4)
        match code[pc] % 100:
            case 1:
                code[out(3)] = get(1) + get(2)
                pc += 4
            case 2:
                code[out(3)] = get(1) * get(2)
                pc += 4
            case 3:
                while True:
                    try:
                        n = next(inp)
                    except StopIteration:
                        # not sure about this. :(
                        yield "wait"
                    else:
                        break
                code[out(1)] = n
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
            case 9:
                rb += get(1)
                pc += 2
            case 99:
                break
            case x:
                print(f'instruction {x}')
    #print(len(code))

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
        while channel:
            yield channel.popleft()

    return send, run(code, recv())
