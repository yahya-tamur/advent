from common import get_problem
import re


part1 = '|'.join([str(i) for i in range(10)])

nums = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
nums = [(i+1, n) for i, n in enumerate(nums)]
part2 = "(0)|" + '|'.join([f'({n}|{i})' for i, n in nums])
part2r = "(0)|" + '|'.join([f'({n[::-1]}|{i})' for i, n in nums])

get_num = {str(i) : i for i in range(10)} \
        | {n:i for i,n in nums} \
        | {n[::-1] : i for i, n in nums}


ans1 = 0
ans2 = 0
for s in get_problem(2023, 1).split('\n'):
    if not s:
        continue
    l = get_num[re.search(part1, s)[0]]
    r = get_num[re.search(part1, s[::-1])[0]]
    l_ = get_num[re.search(part2, s)[0]]
    r_ = get_num[re.search(part2r, s[::-1])[0]]

    ans1 += int(l)*10 + int(r)
    ans2 += int(l_)*10 + int(r_)

print(f"part 1: {ans1}")
print(f"part 2: {ans2}")
