from common import gpl

nums = [int(i) for i in gpl()]

nums.append(0)
nums.append(max(nums)+3)

nums.sort()

one, three = 0, 0

for i in range(len(nums)-1):
    match nums[i+1] - nums[i]:
        case 3:
            three += 1
        case 1:
            one += 1
        case 0:
            print("duplicate")

print(f"part 1: {one*three}")

ways = [1]

for i in range(1,len(nums)):
    ways.append(0)
    for j in range(max(i-3,0), i):
        if nums[i] - nums[j] <= 3:
            ways[-1] += ways[j]

print(f"part 2: {ways[-1]}")

