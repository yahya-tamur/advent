from problem import get_problem_lines

ans1 = 0
ans2 = 0

def safe(nums):
    d = nums[1] - nums[0]
    return all(d*nums[i] < d*nums[i+1] and nums[i+1] - nums[i] in (-3, -2, -1, 1, 2, 3) for i in range(len(nums) - 1))

for line in get_problem_lines():
    nums = [int(x) for x in line.split(' ')]

    ans1 += safe(nums)
    ans2 += any(safe(nums[:i] + nums[i+1:]) for i in range(len(nums)))


print(f"part 1: {ans1}")
print(f"part 2: {ans2}")
