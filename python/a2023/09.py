from common import get_problem_lines

seqs = [[int(x) for x in line.split(' ')] for line in get_problem_lines()]

ans1, ans2 = 0, 0
for seq in seqs:
    diffs = [seq]
    while not all([x == 0 for x in diffs[-1]]):
        diffs.append([diffs[-1][i+1] - diffs[-1][i] for i in range(len(diffs[-1])-1)])
    ans1 += sum([d[-1] for d in diffs])
    ans2 += sum([d[0]*((-1) ** i) for i, d in enumerate(diffs)])

print(f"part 1: {ans1}")
print(f"part 2: {ans2}")
