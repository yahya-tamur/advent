from problem import get_problem, get_problem_lines
from functools import cmp_to_key

inp = get_problem()

l, r = inp.split('\n\n')


ll = []
for line in l.split('\n'):
    x, y = line.split('|')
    ll.append((int(x), int(y)))

ans = 0
ans2 = 0
for line in r.split('\n'):
    nums = [int(x) for x in line.split(',') if x]
    if not nums:
        continue
    conums = {x : i for (i, x) in enumerate(nums)}

    if all((x not in conums) or (y not in conums) or conums[x] < conums[y] \
            for (x, y) in ll):
        ans += nums[len(nums) // 2]
    else:
        nums.sort(key=cmp_to_key(lambda x,y: 2*((x, y) in ll) - 1))
        ans2 += nums[len(nums) // 2]






print(f"part 1: {ans}")
print(f"part 2: {ans2}")
