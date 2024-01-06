from problem import gp
from functools import reduce

part1 = 0
part2 = 0
for i in gp().strip().split('\n\n'):
    part1 += len(set(i.replace('\n','')))
    part2 += len(reduce(lambda a, b: a&b, [set(s) for s in i.split('\n')]))

print(f"part 1: {part1}")
print(f"part 2: {part2}")
