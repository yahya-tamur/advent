import re

from problem import get_problem

inp = get_problem()


def process(s):
    ans = 0
    for x in re.findall(r"mul\(\d+,\d+\)", s):
        t = x.find(',')
        l, r = x[4:t], x[t+1:-1]
        ans += int(l)*int(r)
    return ans

print(f"part 1: {process(get_problem())}")

inp = get_problem()

i = 0

ans = 0

while True:
    j = inp.find("don't()", i)
    if j == -1:
        ans += process(inp[i:])
        break
    ans += process(inp[i:j])

    i = inp.find("do()", j)

print(f"part 2: {ans}")
