from problem import get_problem_lines

perimeter = 0
integral = 0
depth = 0
for line in get_problem_lines(file="input"):
    dir, num, color = line.split(' ')
    num = int(num)
    match dir:
        case 'U':
            depth -= num
        case 'D':
            depth += num
        case 'L':
            integral += depth*num
        case 'R':
            integral -= depth*num
    perimeter += num

area = abs(integral) + (perimeter // 2 + 1)

print(f"part 1: {area}")

perimeter = 0
# I really liked Green's Theorem when I first learned it, but in hindsight
# it's not that difficult to see why it works, especially in this simple case.
integral = 0
depth = 0
for line in get_problem_lines(file="input"):
    _, _, color = line.split(' ')
    color = color[2:-1]
    color = int(color, 16)
    dir = color % 4
    num = color >> 4
    match dir:
        case 3:
            depth -= num
        case 1:
            depth += num
        case 2:
            integral += depth*num
        case 0:
            integral -= depth*num
    perimeter += num

area = abs(integral) + (perimeter // 2 + 1)

print(f"part 2: {area}")
