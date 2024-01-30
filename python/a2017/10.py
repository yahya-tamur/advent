from problem import gp

lst = list(range(256))
skip = 0
start = 0

for l in gp().split(','):
    l = int(l)
    print(l)
    if l != 0:
        lst = lst[l-1::-1] + lst[l:]
    print("r", lst)
    cut = (l+skip) % len(lst)
    print("cut", cut)
    lst = lst[cut:] + lst[:cut]
    start -= cut
    skip += 1
    print(lst)

print(f"part 1: {lst[start % len(lst)]*lst[(start+1)% len(lst)]}")
