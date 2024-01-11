# put it in common/problem?
def get_code(*args, **kwargs):
    from problem import gp
    return [int(i) for i in gp(*args, **kwargs).strip().split(',')]

# generator -> generator of lists
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
    def _set(i, val):
        match (code[pc] // (10 ** (i+1))) % 10:
            case 0:
                extend_to(code[pc+i])
                code[code[pc+i]] = val
            case 2:
                extend_to(code[pc+i]+rb)
                code[code[pc+i]+rb] = val
            case n:
                print(f'mode {n}')
    input_index = 0
    pc = 0
    rb = 0
    output = list()
    while True:
        extend_to(pc+4)
        match code[pc] % 100:
            case 1:
                _set(3, get(1) + get(2))
                pc += 4
            case 2:
                _set(3, get(1) * get(2))
                pc += 4
            case 3:
                yield output
                output = list()
                _set(1, next(inp))
                pc += 2
            case 4:
                output.append(get(1))
                pc += 2
            case 5:
                pc = get(2) if get(1) else pc + 3
            case 6:
                pc = get(2) if not get(1) else pc + 3
            case 7:
                _set(3, int(get(1) < get(2)))
                pc += 4
            case 8:
                _set(3, int(get(1) == get(2)))
                pc += 4
            case 9:
                rb += get(1)
                pc += 2
            case 99:
                break
            case x:
                print(f'instruction {x}')
    yield output

#list -> list
def execute(code, inp):
    ans = list()
    for a in run(code, iter(inp)):
        ans.extend(a)
    return ans

#() -> init, sendrecv
def interact(code):
    from collections import deque
    channel = deque()

    def recv():
        while True:
            yield channel.popleft()

    c = run(code, recv())
    out = next(c)
    def sendrecv(i):
        channel.append(i)
        return next(c, None)

    return out, sendrecv
