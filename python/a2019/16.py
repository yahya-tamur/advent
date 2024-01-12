from problem import gp

# Took me a long time! getting this relatively fasy loop with the cumulative
# sums took a while, then I finally got it to run in a reasonable time when I
# realized we don't need to bother with the first n signals at all if we're
# only going to look at signals n through n+8 at the end.

# Then I read on reddit that the part of the pattern we're looking at for part 2
# is all 1's !!! !!! The solution I came up with is still as fast as solutions
# using that property though, maybe up to a constant factor.
def run(signal, off):
    cumsum = [0 for _ in signal] + [0]
    cumsum_ = [0 for _ in signal] + [0]
    for i, x in enumerate(signal):
        cumsum[i+1]= cumsum[i] + x

    for i in range(100):
        for m in range(len(signal)):
            sgn = 1
            ans = 0
            i = m
            while i < len(signal):
                if i+(m+off)+1 >= len(signal):
                    ans += (cumsum[-1] - cumsum[i])*sgn
                    break
                ans += (cumsum[i+(m+off)+1] - cumsum[i])*sgn
                sgn *= -1
                i += 2*(m+off)+2
            cumsum_[m+1] = int(str(ans)[-1]) + cumsum_[m]
        cumsum, cumsum_ = cumsum_, cumsum
    return ''.join((str(i-j) for i,j, _ in zip(cumsum[1:], cumsum[:-1], range(8))))


inp = gp().strip()
num = int(inp[:7])
inp = [int(x) for x in inp]
print(f"part 1: {run(inp, 0)}")

signal = (inp* 10000)[num:]

print(f"part 2: {run(signal, num)}")
