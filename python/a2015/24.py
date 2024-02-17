from problem import gpl

# Similar idea as day 17.
# Also, I first get all groups with sum equal to sum(input) // (3 or 4)
# Then pick the best one, then do the expensive check of
# "can I split the rest of the elements into (2 or 3) even parts?"
# Or equivalently, "is there (one or two) other groups with the same
# sum, such that they're all pairwise disjoint?"
# Luckily we quickly get the answer 'yes', because the check is
# O(50_000 * 50_000) for part 2.


nums = [int(line) for line in gpl()]
m = sum(nums) // 3
d = {i: set() for i in range(m + 1)}
d[0] = {()}

for n in nums:
    d_ = {i: d[i].copy() for i in range(n)}
    for i in range(n, m+1):
        d_[i] = d[i] | {s + (n,) for s in d[i - n]}
    d = d_

def score(s):
    prod = 1
    for p in s:
        prod *= p
    return (len(s), prod)

ans = -1
dontinclude = []
while True:
    ans = min((x for x in d[m] if x not in dontinclude), key=score)
    if any(len(set(x) & set(ans)) == 0 for x in d[m]):
        break
    dontinclude.append(ans)
print(f"part 1: {score(ans)[1]}")

m = sum(nums) // 4
ans = -1
dontinclude = []
while True:
    ans = min((x for x in d[m] if x not in dontinclude), key=score)
    if any(len(set(x) & set(ans)) == 0 and \
            len(set(x) & set(y)) == 0 and \
            len(set(ans) & set(y)) == 0 \
            for x in d[m] for y in d[m]):
        break
    dontinclude.append(ans)
print(f"part 2: {score(ans)[1]}")

