from common import get_problem
import re

input = get_problem(2021, 17)
#input = "target area: x=20..30, y=-10..-5\n"

m = re.match(".*x=(?P<x1>.*)\.\.(?P<x2>.*),.*y=(?P<y1>.*)\.\.(?P<y2>.*)\n",
             input)

x1 = int(m.group('x1'))
x2 = int(m.group('x2'))
y1 = int(m.group('y1'))
y2 = int(m.group('y2'))

if x1 <= 0 or x1 > x2 or y2 >= 0 or y1 > y2:
    print("NOT IMPLEMENTED!!")

# I spent way too much time trying to think of a 'better' solution

y_max = 0
num_ways = 0

for xv in range(x2+5):
    for yv in range(-abs(y1)-5,abs(y1)+5):
        xv_ = xv
        yv_ = yv
        x = 0
        y = 0
        this_y_max = y
        while x <= x2 + 5 and y >= y1 - 5:
            if x1 <= x and x <= x2 and y1 <= y and y <= y2:
                num_ways += 1
                y_max = max(y_max, this_y_max)
                break
            x += xv_
            y += yv_
            this_y_max = max(this_y_max,y)
            if xv_ > 0:
                xv_ -= 1
            yv_ -= 1

print(f'part 2: {y_max}')
print(f'part 2: {num_ways}')
        

