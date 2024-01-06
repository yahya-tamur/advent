from problem import gpl

# -1 in python is very cool for bitwise operations.

himask = 0 # 0 if if shouldn't do anything, 1 if it should set to 1
lomask = -1 # 1 if it shouldn't do anything, 0 if it should set to 0
mask = "asdf"

def get_addrs(address, mask):
    wildcards = [i for i in range(36) if mask[35-i] == 'X']
    answers = [address | int(mask.replace('X','0'),base=2)]
    for i in wildcards:
        answers_ = [(1 << i) ^ a for a in answers]
        answers_.extend(answers) #rust...
        answers = answers_
    return answers


mem1 = dict()
mem2 = dict()
for line in gpl():
    if 'mask' in line:
        himask = int(line[-36:].replace('X','0'), base=2)
        lomask = int(line[-36:].replace('X','1'), base=2)
        mask = line[-36:]
        continue
    loc, val = int(line[4:line.find(']')]), int(line[line.find('=')+2:])
    mem1[loc] = (val | himask) & lomask
    for addr in get_addrs(loc, mask):
        mem2[addr] = val


print(f"part 1: {sum(mem1.values())}")
print(f"part 2: {sum(mem2.values())}")
