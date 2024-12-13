from problem import get_problem, get_problem_lines

gpl = list(get_problem_lines())

def solve(part):
    ans = 0

    i = 0
    while i + 2 < len(gpl):
        ax, ay = int(gpl[i][12:14]), int(gpl[i][18:])
        i += 1
        bx, by = int(gpl[i][12:14]), int(gpl[i][18:])
        i += 1
        px = int(gpl[i][gpl[i].find('=')+1:gpl[i].find(',')])
        py = int(gpl[i][gpl[i].rfind('=')+1:])
        i += 1

        if part == 2:
            px += 10000000000000
            py += 10000000000000


        dt = ax*by - ay*bx

        s1 = (by*px - bx*py) / dt
        s2 = (-ay*px + ax*py) / dt

        if part == 1:
            if s1 in range(101) and s2 in range(101):
                ans += 3*s1 + s2
        else:
            if s1 >= 0 and s1 == int(s1) and s2 >= 2 and s2 == int(s2):
                ans += 3*s1 + s2
    return int(ans)


print(f"part 1: {solve(1)}")
print(f"part 2: {solve(2)}")
