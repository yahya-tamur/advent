from problem import gp

inp = [ord(c) for c in gp().strip()]

def incr(l):
    i, carry = 0, True

    while carry:
        carry = False
        i -= 1
        l[i] += 1
        while l[i] in (ord('o'), ord('i'), ord('l')):
            l[i] += 1
        if l[i] > ord('z'):
            l[i] = ord('a')
            carry = True

def find():
    while True:
        c1 = any(inp[i]+1 == inp[i+1] and inp[i]+2 == inp[i+2] for i in range(len(inp)-2))

        l = [i for i in range(len(inp)-1) if inp[i] == inp[i+1]]

        c3 = l and l[-1] - l[0] >= 2

        if c1 and c3:
            return ''.join(chr(c) for c in inp)

        incr(inp)

print(f"part 1: {find()}")

incr(inp)

print(f"part 2: {find()}")


