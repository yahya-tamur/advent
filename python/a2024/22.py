from problem import get_problem, get_problem_lines, look
from collections import defaultdict

secret = 123

def step(n):
    n = (((n*64) ^ n) % 16777216)
    n = ((n // 32) ^ n) % 16777216
    n = ((n * 2048) ^ n) % 16777216
    return n

ans = 0
for line in get_problem_lines():
    n = int(line)
    for _ in range(2000):
        n = step(n)
    ans += n

print(f"part 1: {ans}")


d = defaultdict(int)

for line in get_problem_lines():
    n = int(line)
    window = tuple()
    for _ in range(4):
        n_ = step(n)
        window += ((n_ % 10) - (n % 10),)
        n = n_

    seen_now = set()
    for i in range(1996):

        if window not in seen_now:
            d[window] += n % 10
            seen_now.add(window)

        n_ = step(n)
        window = window[1:] + (((n_ % 10) - (n % 10)),)
        n = n_

print(f"part 2: {max(d.values())}")

