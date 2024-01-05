from common import gpl

def search(target):
    val = 1
    i = 0
    while val != target:
        val = val*7 % 20201227
        i += 1
    return i

a, b = gpl()

print(f"part 1: {pow(int(b), search(int(a)), 20201227)}")
