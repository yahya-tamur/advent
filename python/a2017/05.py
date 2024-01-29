from problem import gpl

def run(part):
    code = [int(x) for x in gpl()]
    i, k = 0, 0
    while i in range(len(code)):
        k += 1
        # Apparently you can't do simultaneous assignment with lists
        i_ = i + code[i]
        code[i] = code[i] + 1 - 2*part*(code[i] >= 3)
        i = i_
    return k

print(f"part 1: {run(0)}")
print(f"part 2: {run(1)}")


