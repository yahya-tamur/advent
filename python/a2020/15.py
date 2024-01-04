from common import gp

input = [int(i) for i in gp().strip().split(',')]

def solve(n):
    i, on, lastseen = len(input)-1, input[-1], {n: i for i, n in enumerate(input[:-1])}
    while i < n - 1:
        i, lastseen[on], on = i+1, i, 0 if on not in lastseen else i - lastseen[on]
    return on

print(f"part 1: {solve(2020)}")
print(f"part 2: {solve(30000000)}")

# I was a little disappointed the answer to part 2 is just brute forcing.
# But pretty interesting sequence 'Van Eck'
