from problem import gp

inss = gp().strip().split(',')

def init():
    return [chr(c+ord('a')) for c in range(16)]

def run(line):
    for ins in inss:
        match ins[0]:
            case 's':
                v = int(ins[1:])
                line = line[-v:] + line[:-v]
            case 'x':
                a, b = int(ins[1:ins.find('/')]), int(ins[1+ins.find('/'):])
                line[b], line[a] = line[a], line[b]
            case 'p':
                a, b = ins[1], ins[3]
                i, j = next((i for i, c in enumerate(line) if c == a)), \
                        next((i for i, c in enumerate(line) if c == b))
                line[i], line[j] = b, a
    return line

print(f"part 1: {''.join(run(init()))}")

line = init()
seen = dict()

for i in range(1_000_000_000):
    encoded = ''.join(line)
    if encoded in seen:
        break
    seen[encoded] = i
    line = run(line)
start, loop = seen[encoded], i
i = (1_000_000_000 - start) % (loop - start)

print(f"part 2: {''.join(next((line for line, i_ in seen.items() if i == i_)))}")

