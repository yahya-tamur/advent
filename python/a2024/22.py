from problem import get_problem, get_problem_lines, look
from collections import defaultdict
from time import time
#aaa = time()

def step(n):
    n = ((n * 64) ^ n) % 16777216
    n = ((n // 32) ^ n) % 16777216
    n = ((n * 2048) ^ n) % 16777216
    return n

ans1 = 0
d = defaultdict(int)

for line in get_problem_lines():
    n = int(line)
    window = 0
    for _ in range(4):
        n_ = step(n)
        window = window*20 + ((n_ % 10) - (n % 10) + 10)
        n = n_

    seen_now = set()
    for i in range(1997):
        if i == 1996:
            ans1 += n

        if window not in seen_now:
            d[window] += n % 10
            seen_now.add(window)

        n_ = step(n)
        window = (window*20 + ((n_ % 10) - (n % 10) + 10)) % (20 ** 4)
        n = n_

#print(time() - aaa)
print(f"part 1: {ans1}")
print(f"part 2: {max(d.values())}")
