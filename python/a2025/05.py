from problem import get_problem, get_problem_lines, look

ranges, inputs = get_problem().strip().split('\n\n')

ranges = [eval(line.replace('-',',')) for line in ranges.split('\n')]

ranges.sort()

# O(n) not O(n^2) by making new list, not removing elements in place
# though n is 190 in this case

ranges_ = []
for i in range(len(ranges)-1):
    if ranges[i+1][0]-1 <= ranges[i][1]:
        ranges[i+1] = (ranges[i][0], max(ranges[i][1], ranges[i+1][1]))
    else:
        ranges_.append(ranges[i])

ranges_.append(ranges[-1])
ranges = ranges_

print(f"part 1: {sum(any(int(i) in range(l,r+1) for l,r in ranges) for i in inputs.split(chr(10))) }")
print(f"part 2: {sum(r+1-l for l, r in ranges)}")

