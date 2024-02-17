from math import ceil, sqrt
from collections import defaultdict

primes = [2,3,5]

def extend_primes(n):
    global primes
    while primes[-1] < n:
        num = primes[-1] + 2

        while True:
            i = 1
            prime = True
            while primes[i] <= ceil(sqrt(num))+1:
                if num % primes[i] == 0:
                    prime = False
                    break
                i += 1
            if not prime:
                num += 2
                continue
            primes.append(num)
            break

def solve(n):
    pfac = defaultdict(int)

    extend_primes(ceil(sqrt(n))+1)

    i = 0
    while n != 1:
        if primes[i] > ceil(sqrt(n)):
            pfac[n] += 1
            break
        while n % primes[i] == 0:
            pfac[primes[i]] += 1
            n //= primes[i]

        i += 1

    pfac = list(pfac.items())

    def collect(ps, i):
        if i == len(pfac):
            return ps
        else:
            p, n = pfac[i]
            pn = 1
            ans = 0
            for _ in range(n+1):
                ans += collect(ps*pn, i+1)
                pn *= p
            return ans

    return collect(1, 0)

from problem import gp
inp = int(gp())

p1 = 1
while solve(p1)*10 < inp:
    p1 += 1

print(f"part 1: {p1}")

from collections import defaultdict
doors = defaultdict(int)
p2 = 999999999999

i = 0
while i < p2:
    for j in range(1, 51):
        doors[i*j] += i*11
        if doors[i*j] >= inp:
            p2 = min(i*j, p2)
    del doors[i]
    i += 1

print(f"part 2: {p2}")
