from problem import get_problem_lines

s = get_problem_lines()

part1 = 0
part2 = [1 for _ in s]

for (i, ln) in enumerate(s):
    ln = ln.split(':')[1].strip()
    (l, r) = ln.split('|')
    l = {s for s in l.strip().split(' ') if s}
    n = len([x for x in r.split(' ') if x in l])
    if n:
        for k in range(i+1,min(i+n+1,len(s))):
            part2[k] += part2[i]
        part1 += 2 ** (n-1)

print(f"part 1: {part1}")
print(f"part 2: {sum(part2)}")
