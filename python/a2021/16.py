from common import get_problem

input = get_problem()
#input = "9C0141080250320F1802104A08"
# convert to binary
hdict = dict()
for i in range(10):
    hdict[chr(ord('0')+i)] = i
for i in range(6):
    hdict[chr(ord('A')+i)] = 10 + i
l = list()
for h in input:
    if (v := hdict.get(h)) is not None:
        l.append(int(bool(v & 8)))
        l.append(int(bool(v & 4)))
        l.append(int(bool(v & 2)))
        l.append(int(bool(v & 1)))

def read_bin(l, start, n):
    ans = 0
    for j in range(n):
        ans = ans*2 + l[start+j]
    return ans

def prod(l):
    ans = 1
    for i in l:
        ans *= i
    return ans

ops = [sum, prod, min, max, 'no', lambda l: int(l[0]>l[1]), lambda l: int(l[0]<l[1]),
       lambda l: int(l[0]==l[1])]

vsum = 0
i = 0
def read_packet():
    global vsum, i
    ver = read_bin(l,i,3)
    vsum += ver
    id = read_bin(l,i+3,3)
    if id == 4:
        i += 6
        ans = list()
        while True:
            ans += l[i+1:i+5]
            i += 5
            if l[i-5] != 1:
                break
        return read_bin(ans,0, len(ans))
    else:
        lt = l[i+6]
        if l[i+6]:
            num_packets = read_bin(l, i+7, 11)
            i = i+18
            vals = list()
            for _ in range(num_packets):
                vals.append(read_packet())
            return(ops[id](vals))
        else:
            end = i + 22 + read_bin(l, i+7, 15)
            i = i+22
            vals = list()
            while i < end:
                vals.append(read_packet())
            return(ops[id](vals))



part2 = read_packet()
print(f"part 1: {vsum}")
print(f"part 2: {part2}")


