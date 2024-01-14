from problem import gp

def trim(s):
    s_ = []
    i = 0
    while i < len(s):
        s_.append(s[i])
        cl, cr = len(s_)-1, i+1

        while cl >= 0 and cr < len(s) and abs(s_[cl] - s[cr]) == ord('a') - ord('A'):
            cl -= 1
            cr += 1

        while len(s_) > cl + 1:
            s_.pop()

        i = cr

    return len(s_)

s = [ord(c) for c in gp().strip()]

p2 = min((trim([x for x in s if x != c+ord('a') and x != c+ord('A')]) for c in range(26)))
print(f"part 1: {trim(s)}")
print(f"part 2: {p2}")
