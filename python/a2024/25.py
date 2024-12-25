from problem import get_problem, get_problem_lines, look


locks, keys = [], []

for lk in get_problem().split('\n\n'):
    lk = [line for line in lk.split('\n') if line]

    nums = [sum(x[i] == '#' for x in lk) - 1 for i in range(5)]
    if lk[0][0] == '#':
        locks.append(nums)
    else:
        keys.append(nums)

ans = 0
for key in keys:
    for lock in locks:
        ans += all(n + m <= 5 for (n, m) in zip(key, lock))

print(f"part 1: {ans}")
print(f"part 2: {0}")
