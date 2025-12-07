from problem import get_problem, get_problem_lines, look
from collections import defaultdict

lines = [{i for i, c in enumerate(line) if c != '.'} for line in get_problem_lines()]

beams = {c : 1 for c in lines[0]}
print(beams)

p1 = 0
for i in range(1, len(lines)):
    beams_ = defaultdict(int)
    for b, bb in beams.items():
        if b in lines[i]:
            beams_[b-1] += bb
            beams_[b+1] += bb
            p1 += 1 
        else:
            beams_[b] += bb

    beams = beams_


print(f"part 1: {p1}")
print(f"part 2: {sum(beams.values())}")
