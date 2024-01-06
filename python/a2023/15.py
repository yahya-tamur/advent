from problem import get_problem

def score(word):
    ans = 0
    for c in word:
        ans += ord(c)
        ans *= 17
        ans %= 256
    return ans

def rm(box, word):
    for i in range(len(box)):
        if box[i][0] == word:
            box.pop(i)
            return

def add(box, word, num):
    for i in range(len(box)):
        if box[i][0] == word:
            box[i] = (word, num)
            return
    box.append((word,num))

def parse(instr):
    if '-' in instr:
        word = instr[:-1]
        return (score(word), word)
    word=instr[:-2]
    return (score(word), word, instr[-1])

input = get_problem()[:-1].split(',')
input = [i for i in input if i]

part1 = 0
hm = [[] for _ in range(256)]
for word in input:
    part1 += score(word)
    parsed = parse(word)
    if len(parsed) == 2:
        (box, label) = parsed
        rm(hm[box], label)
    else:
        (box, label, num) = parsed
        add(hm[box], label, num)

part2 = 0
for i, box in enumerate(hm):
    for j, (_, num) in enumerate(box):
        part2 += (i+1)*(j+1)*int(num)

print(f"part 1: {part1}")
print(f"part 2: {part2}")


