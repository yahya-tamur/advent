from intcode import execute, get_code, interact

# Very unusual for aoc -- it's usually programming-language agnostic.
#
# Finding the actual answer to where to jump requires looking at the whole
# road. Ex: ###.#.#.#.#.# (...) #.#.#...###########
# You need to know if the pattern repeats an odd or even number of times.
# I would expect an aoc problem to give you the whole road, then ask for 
# where the jumps are or something.


def read_sc(sc):
    return [ord(c) for c in sc[1:]]

# jump if: there's a hole before D and D is ground.
springcode = """
OR A J
AND B J
AND C J
NOT J J
AND D J
WALK
"""

def po(ddd):
    if ddd is None:
        print('None')
        return
    for c in ddd:
        if c > 256:
            print(f'${c}',end='')
        else:
            print(chr(c),end='')

print(f"part 1: {execute(get_code(), read_sc(springcode))[-1]}")

#jump if: D is ground AND there's a hole before D AND (D+1) is fine or D+4 is fine

#OR E T; AND E T; sets T to E. First sets if E is true, second sets if it's false.
springcode = """
OR D J
OR A T
AND B T
AND C T
NOT T T
AND T J
OR E T
AND E T
OR H T
AND T J
RUN
"""



print(f"part 2: {execute(get_code(), read_sc(springcode))[-1]}")
