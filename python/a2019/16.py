from problem import gp

signal = [int(x) for x in gp().strip()]*10000
base = [0, 1, 0, -1]

#ith element of the nth pattern
def pattern(n, i):
    n = n+1
    i = (i + 1)
    return base[(i % (4*n)) // n]

signal_ = [0 for _ in signal]
for i in range(100):
    print(i)
    for n in range(len(signal)):
        ans = 0
        for m in range(len(signal)):
            ans += pattern(n,m)*signal[m]
        signal_[n] = int(str(ans)[-1])
    signal = signal_
print(f"part 1: {''.join((str(c) for c in signal[:8]))}")



