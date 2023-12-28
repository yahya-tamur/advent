from common import get_problem_lines

lines = get_problem_lines()

processes = dict()

def run_range(process, x0, x1, m0, m1, a0, a1, s0, s1):
    if process == 'R' or x0 >= x1 or m0 >= m1 or a0 >= a1 or s0 >= s1:
        return 0
    if process == 'A':
        return (x1-x0)*(m1-m0)*(a1-a0)*(s1-s0)
    ans = 0
    for line in processes[process]:
        if line.find(':') != -1:
            num = int(line[2:line.find(':')])
            match line[0], line[1]:
                case 'x', '<':
                    num = min(x1, num)
                    ans += run_range(line[line.find(':')+1:], x0, num, m0, m1, a0, a1, s0, s1)
                    x0 = num
                case 'm', '<':
                    num = min(m1, num)
                    ans += run_range(line[line.find(':')+1:], x0, x1, m0, num, a0, a1, s0, s1)
                    m0 = num
                case 'a', '<':
                    num = min(a1, num)
                    ans += run_range(line[line.find(':')+1:], x0, x1, m0, m1, a0, num, s0, s1)
                    a0 = num
                case 's', '<':
                    num = min(s1, num)
                    ans += run_range(line[line.find(':')+1:], x0, x1, m0, m1, a0, a1, s0, num)
                    s0 = num
                case 'x', '>':
                    num = max(x0, num+1)
                    ans += run_range(line[line.find(':')+1:], num, x1, m0, m1, a0, a1, s0, s1)
                    x1 = num
                case 'm', '>':
                    num = max(m0, num+1)
                    ans += run_range(line[line.find(':')+1:], x0, x1, num, m1, a0, a1, s0, s1)
                    m1 = num
                case 'a', '>':
                    num = max(a0, num+1)
                    ans += run_range(line[line.find(':')+1:], x0, x1, m0, m1, num, a1, s0, s1)
                    a1 = num
                case 's', '>':
                    num = max(s0, num+1)
                    ans += run_range(line[line.find(':')+1:], x0, x1, m0, m1, a0, a1, num, s1)
                    s1 = num
        else:
            ans += run_range(line, x0, x1, m0, m1, a0, a1, s0, s1)
            return ans


def run(process, x, m, a, s):
    if process == 'A':
        return True
    if process == 'R':
        return False
    for line in processes[process]:
        if line.find(':') != -1:
            if eval(line[:line.find(':')]):
                return run(line[line.find(':')+1:], x, m, a, s)
        else:
            return run(line, x, m, a, s)

part1 = 0
for line in lines:
    if line[0] == '{':
        x = int(line[line.find('x')+2:line.find(',', line.find('x'))])
        m = int(line[line.find('m')+2:line.find(',', line.find('m'))])
        a = int(line[line.find('a')+2:line.find(',', line.find('a'))])
        s = int(line[line.find('s')+2:line.find('}', line.find('s'))])
        if run('in', x, m, a, s):
            part1 += x + m + a + s
    else:
        processes[line[:line.find('{')]] = line[line.find('{')+1:-1].split(',')

print(f"part 1: {part1}")
print(f"part 2: {run_range('in', 1, 4001, 1, 4001, 1, 4001, 1, 4001)}")

