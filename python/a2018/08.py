from problem import gp

nums = [int(x) for x in gp().strip().split(' ')]

i = 0

p1 = 0
# returns end index
def read_node(start):
    global p1
    chs = nums[start]
    mts = nums[start+1]
    i = start + 2
    chvals = list()
    ans = 0
    for _ in range(chs):
        i, v = read_node(i)
        chvals.append(v)
    for j in range(mts):
        p1 += nums[i+j]
    if chvals:
        for j in range(mts):
            if nums[i+j]-1 < len(chvals):
                ans += chvals[nums[i+j]-1]
    else:
        for j in range(mts):
            ans += nums[i+j]
    return (i + mts, ans)

_, p2 = read_node(0)

print(f"part 1: {p1}")
print(f"part 2: {p2}")

