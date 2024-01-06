from problem import get_problem_lines
from collections import Counter

def star(states):
    ans = Counter()
    for (i, nums), n in states.items():
        if nums and i+1 <= nums[0]:
            ans[(i+1,nums)] += n
    return ans

def dot(states):
    ans = Counter()
    for (i, nums),n in states.items():
        if i == 0:
            ans[(0, nums)] += n
        else:
            if nums and i == nums[0]:
                ans[(0, nums[1:])] += n
    return ans

def solve(seq, nums):
    seq = seq + ['.'] # simplifies accept case
    states = Counter([(0, nums)])
    for c in seq:
        match c:
            case '#':
                states = star(states)
            case '.':
                states = dot(states)
            case '?':
                states = star(states) + dot(states)
            case _:
                print('Nooo')
    return states[(0,())]

ans1, ans2 = 0, 0
for line in get_problem_lines():
    (seq, nums) = line.split(' ')
    nums = tuple(eval(nums))
    seq = list(seq)
    ans1 += solve(seq, nums)
    ans2 += solve((seq + ['?'])*4+seq, nums*5)

print(f"part 1: {ans1}")
print(f"part 2: {ans2}")
