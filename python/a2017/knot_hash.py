def run(ll, rounds=1):
    lst = list(range(256))
    skip = 0
    start = 0
    for _ in range(rounds):
        for l in ll:
            if l != 0:
                lst = lst[l-1::-1] + lst[l:]
            cut = (l+skip) % len(lst)
            lst = lst[cut:] + lst[:cut]
            start -= cut
            skip += 1
    start = start % len(lst)

    return lst[start:] + lst[:start]

def knot_hash(s):
    lst = run([ord(c) for c in s] + [17, 31, 73, 47, 23], rounds=64)

    dense = list()

    for i in range(0,255,16):
        dense.append(0)
        for j in lst[i:i+16]:
            dense[-1] ^= j

    return dense


