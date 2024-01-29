from problem import gpl

print(f"part 1: {sum((len(set(p)) == len(p) for p in (line.split(' ') for line in gpl())))}")
print(f"part 2: {sum((len({tuple(sorted(x)) for x in p}) == len(p) for p in (line.split(' ') for line in gpl())))}")
