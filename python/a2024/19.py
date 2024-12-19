from problem import get_problem, get_problem_lines

pl = list(get_problem_lines())

steps = pl[0].split(', ')

ans = 0
ans2 = 0
for pattern in pl[1:]:
    ways = [0 for _ in range(len(pattern)+1)]
    ways[0] = 1

    for i in range(len(pattern)+1):
        for step in steps:
            if pattern[i-len(step):i] == step:
                ways[i] += ways[i-len(step)]

    ans += ways[-1] != 0
    ans2 += ways[-1]

print(f"part 1: {ans}")
print(f"part 2: {ans2}")
