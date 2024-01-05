from common import get_problem_lines

ans1, ans2 = 0, 0
for line in get_problem_lines():
    (k, k_, k__) = line.find('-'), line.find(' '), line.find(': ')
    (l, r, c, p) = int(line[:k]), int(line[k+1:k_]), line[k_+1:k__], line[k__+2:]
    if len([1 for x in p if x == c]) in range(l,r+1):
        ans1 += 1
    if sum([ p[i-1] == c for i in [l,r]]) == 1:
        ans2 += 1
print(f"part 1: {ans1}")
print(f"part 2: {ans2}")
