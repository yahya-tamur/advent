from problem import gpl

def part1():
    lst = [3,7]

    elfa = 0
    elfb = 1

    after = int(gpl()[0])

    while len(lst) < after + 10:
        sum = lst[elfa] + lst[elfb]
        if sum >= 10:
            lst.append(sum // 10)
        lst.append(sum % 10)

        elfa = (elfa + lst[elfa] + 1) % len(lst)
        elfb = (elfb + lst[elfb] + 1) % len(lst)

    return ''.join((str(lst[i]) for i in range(after,after+10)))

#it's a little slow, maybe there's a better way of doing it.
def part2():
    lst = [3,7]

    elfa = 0
    elfb = 1

    after = [int(i) for i in gpl()[0]]

    while True:
        sum = lst[elfa] + lst[elfb]
        if sum >= 10:
            lst.append(sum // 10)
        lst.append(sum % 10)

        elfa = (elfa + lst[elfa] + 1) % len(lst)
        elfb = (elfb + lst[elfb] + 1) % len(lst)

        if lst[-len(after):] == after:
            return len(lst) - len(after)
        if lst[-len(after)-1:-1] == after:
            return len(lst) - len(after)-1

print(f"part 1: {part1()}")
print(f"part 2: {part2()}")
