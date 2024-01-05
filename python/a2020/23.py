from common import gp
from collections import deque

class Solve:
    def __init__(self, cups):
        l = [0 for _ in range(len(cups)+1)]
        r = [0 for _ in range(len(cups)+1)]
        for ll, rr in zip(cups[:-1], cups[1:]):
            r[ll] = rr
            l[rr] = ll

        l[cups[0]] = cups[-1]
        r[cups[-1]] = cups[0]

        self.l, self.r = l, r
        self.start = cups[0]
        self.highest = max(cups)

    def splice(self, first, last, dest):
        l, r = self.l, self.r #horrible?
        #mend source
        r[l[first]] = r[last]
        l[r[last]] = l[first]

        #attach section
        r[last] = r[dest]
        l[first] = dest

        #attach destination
        l[r[dest]] = last
        r[dest] = first

    def iterate(self, n):
        l, r, current = self.l, self.r, self.start
        for _ in range(n):
            p = [r[current], r[r[current]], r[r[r[current]]]]
            dest = current - 1
            while dest <= 0 or dest in p:
                dest -= 1
                if dest <= 0:
                    dest = self.highest
            self.splice(p[0], p[-1], dest)
            current = r[current]
        return self

    def ans1(self):
        i = self.r[1]
        ans = ""
        while i != 1:
            ans += str(i)
            i = self.r[i]
        return ans

    def ans2(self):
        return self.r[1]*self.r[self.r[1]]


cups = [int(i) for i in gp().strip()]

print(f"part 1: {Solve(cups).iterate(100).ans1()}")

i = max(cups) + 1
while len(cups) < 1000000:
    cups.append(i)
    i += 1

print(f"part 2: {Solve(cups).iterate(10000000).ans2()}")
