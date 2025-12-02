from problem import get_problem, get_problem_lines, look

def split_interval(l, r):
    ans = []
    ll = l
    m = 10 ** len(str(l))
    for i in range(len(str(l)), len(str(r))):
        ans.append((ll, m-1))
        ll = m
        m = 10*m
    ans.append((ll, r))
    return ans

def solve(l, r, part):
    m = len(str(l))
    ans = set()

    for i in range(2, m+1):
        if m % i != 0:
            continue
        if part == 1 and i > 2:
            break

        n = int(str(l)[:(m // i)])
        rep_n = int(i*str(n))

        while rep_n <= r:
            if rep_n in range(l, r+1):
                ans.add(rep_n)

            n += 1
            rep_n = int(i*str(n))

    return sum(ans)

ans1 = 0
ans2 = 0
total_scan = 0
for lr in get_problem().split(','):
    l, r = lr.split('-')
    l, r = int(l), int(r)
    for l, r in split_interval(l, r):
        ans1 += solve(l, r, 1)
        ans2 += solve(l, r, 2)

print(f"part 1: {ans1}")
print(f"part 2: {ans2}")
