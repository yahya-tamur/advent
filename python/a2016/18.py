from problem import gp

def solve(rows):
    line = ['.'] + list(gp().strip()) + ['.']
    line_ = ['.'] * len(line)

    tile = { \
            ('^','^','.'): '^', \
            ('.','^','^'): '^', \
            ('^','.','.'): '^', \
            ('.','.','^'): '^', \
            ('.','.','.'): '.', \
            ('^','^','^'): '.', \
            ('^','.','^'): '.', \
            ('.','^','.'): '.', \
        }

    ans = line.count('.')

    for _ in range(rows-1):
        for i in range(1, len(line)-1):
            line_[i] = tile[(line[i-1],line[i],line[i+1])]
        line, line_ = line_, line
        ans += line.count('.')

    return ans - rows*2

print(f"part 1: {solve(40)}")
print(f"part 2: {solve(400000)}")
