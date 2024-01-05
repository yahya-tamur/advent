from common import gpl

me, buses = gpl()

# 🌟🌟🌟
# Solution isn't too interesting but I was confused about problems that asked
# something like this in problems I did before.

me = int(me)
buses = [int(bus) for bus in buses.split(',') if bus != 'x']

rem, id = min([(bus - (me % bus), bus) for bus in buses])

print(f"part 1: {rem*id}")

buses2 = [[-i % int(bus), int(bus)] \
        for i, bus in enumerate(gpl()[1].split(',')) if bus != 'x']

# want: smallest n so that all((n % bus[0] = bus[1] for bus in buses2))

# there was always only one element in 'accept'. Is this always the case?
# when everything is relatively prime?
accept, period = [buses2[0][0]], buses2[0][1]

for disp, id in buses2[1:]:
    period_ = id*period
    accept_ = [x+y for x in range(0,period_,period) for y in accept \
            if (x+y)%id == disp]
    period, accept = period_, accept_

print(f"part 2: {min(accept)}")
