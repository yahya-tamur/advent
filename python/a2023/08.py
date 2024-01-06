from problem import get_problem_lines

input = get_problem_lines()

instrs = input[0]

left, right = dict(), dict()

for line in input[1:]:
    left[line[:3]] = line[7:10]
    right[line[:3]] = line[12:15]

def follow(loc, endl):
    i=0
    while not endl(loc):
        loc = left[loc] if instrs[i%len(instrs)] == 'L' else right[loc]
        i += 1
    return i

print(f"part 1: {follow('AAA', lambda x: x == 'ZZZ')}")

# In the data, each start will only reach one end node, and
# the number of steps start -> end = number of steps end -> end

from math import lcm
print(f"part 2: {lcm(*[follow(loc, lambda x: x[-1] == 'Z') for loc in left.keys() if loc[-1] == 'A'])}")
