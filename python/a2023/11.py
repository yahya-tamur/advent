from problem import get_problem_lines

map = [[c == '#' for c in line] for line in get_problem_lines()]

doublerows = [i for i in range(len(map)) if not any(map[i])]
doublecols = [j for j in range(len(map[0])) if \
        not any((map[i][j] for i in range(len(map)))) ]

galaxies = [(i,j) for i in range(len(map)) for j in range(len(map[0])) \
        if map[i][j] ]

ans1, ans2 = 0, 0
for (g1i, g1j) in galaxies:
    for (g2i, g2j) in galaxies:
        if (g1i, g1j) < (g2i, g2j):
            i1, i2 = sorted((g1i, g2i))
            j1, j2 = sorted((g1j, g2j))
            ans1 += i2 - i1 + j2 - j1 + \
                    len([0 for i in doublerows if i1 < i and i < i2]) + \
                    len([0 for j in doublecols if j1 < j and j < j2])
            ans2 += i2 - i1 + j2 - j1 + \
                    999999*len([0 for i in doublerows if i1 < i and i < i2]) + \
                    999999*len([0 for j in doublecols if j1 < j and j < j2])

print(f"part 1: {ans1}")
print(f"part 2: {ans2}")

