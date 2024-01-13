from problem import gpl

#finds a so that ax + by = 1
#REQUIRES: x < y. gcd(x,y) = 1.
def egcd(x, y):
    (a0, b0) = (1, 0) # 1*x + 0*y = x
    (a1, b1) = (0, 1) # 0*x + 1*y = y
    while x != 1:
        d, m = y // x, y % x # if x == 0 here, x and y were 
        (a0, b0, x, a1, b1, y) = (a1 - d*a0, b1 - d*b0, m, a0, b0, x)
    # a0*x_ + b0*y_ = 1
    return a0

def conj(j, size):
    a = egcd(j, size)
    return a % size

def incro(j, target, size):
    #first find the new difference between adjacent elements.
    #0 is at 0, 1 is at j, 2 is a3 j+1, ...
    # ? is at 1 mod size. and that's what conj finds.
    stepsize = conj(j, size)
    #k*(difference between elements) % size = target for which k?
    k = egcd(stepsize, size)
    return k*target % size

def shuffle(current, size):
    for line in gpl():
        if line.find('o') != -1:
            # reverse
            current = size-1 - current
        elif line.find('r') != -1:
            incr = int(line.split(' ')[-1])
            current = incro(incr, current, size)
        else:
            cut = int(line.split(' ')[-1])
            cut = cut % size
            if current < cut:
                current += (size - cut)
            else:
                current -= cut
    return current
print(f"part 1: {shuffle(2019, 10007)}")

rpl = gpl()
rpl.reverse()
def rshuffle(current, size):
    for line in rpl:
        if line.find('o') != -1:
            # reverse
            current = size-1 - current
        elif line.find('r') != -1:
            incr = int(line.split(' ')[-1])
            current = incro(conj(incr, size), current, size)
        else:
            cut = int(line.split(' ')[-1])
            cut = (size - cut) % size
            if current < cut:
                current += (size - cut)
            else:
                current -= cut
    return current

# I had to look at the reddit to figure out how to apply this many times.
# I missed that cut is affine too.

p2size = 119315717514047
a = rshuffle(0, p2size)
b = (rshuffle(1, p2size) - a) % p2size

def apply(n, size, x):
    pb = pow(b, n, size)

    return ((pb-1)*conj(b-1,size)*a + pb*x) % size

print(f"part 2: {apply(101741582076661, p2size, 2020)}")
