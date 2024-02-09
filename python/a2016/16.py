from problem import gp

# I was thinking there might be an interesting solution for this, but this ran
# in a couple of seconds. I didn't even use lists of numbers instead of strings.

def solve(n):
    s = gp().strip()

    while len(s) < n:
        s = s + '0' + s[::-1].replace('0','^').replace('1','0').replace('^','1')

    s = list(s[:n])

    while len(s) % 2 == 0:
        s_ = list()
        for i in range(0, len(s), 2):
            s_.append('1' if s[i] == s[i+1] else '0')
        s = s_

    return ''.join(s)

print(f"part 1: {solve(272)}")
print(f"part 2: {solve(35651584)}")


