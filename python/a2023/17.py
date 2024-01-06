#heapremove turns out o be very inefficient since I was looking through
#the whole heap linearly to find the elements I wanted to remove.

#I also tried to keep a table of minimum costs per state but this is
#unnecessary since I process shortest paths first. We can just keep track of
# which states we've processed.

#I'll use complex numbers for directions next time.

from problem import get_problem_lines
from math import inf
import heapq as h
from sys import exit
from time import time

map = [[int(c) for c in line] for line in get_problem_lines()]

#r, d, l, u = 0, 1, 2, 3

def get_ans(allowed_start, allowed_end):
    def next(i,j,state):
        ans = list()
        if state != 0:
            dc = 0
            for r in range(1, allowed_end):
                if i+r == len(map):
                    break
                dc += map[i+r][j]
                if r >= allowed_start:
                    ans.append((i+r,j,0,dc))
            dc = 0
            for r in range(1, allowed_end):
                if i-r < 0:
                    break
                dc += map[i-r][j]
                if r >= allowed_start:
                    ans.append((i-r,j,0,dc))
        if state != 1:
            dc = 0
            for r in range(1, allowed_end):
                if j+r == len(map[0]):
                    break
                dc += map[i][j+r]
                if r >= allowed_start:
                    ans.append((i,j+r,1,dc))
            dc = 0
            for r in range(1, allowed_end):
                if j-r < 0:
                    break
                dc += map[i][j-r]
                if r >= allowed_start:
                    ans.append((i,j-r,1,dc))
        return ans

    active = [(0,0,0,0), (0,0,0,1)]
    visited = set()
    while True:
        cost, i, j, state = h.heappop(active)
        if (i, j, state) in visited:
            continue
        visited.add((i, j, state))
        if i == len(map)-1 and j == len(map[0])-1:
            return cost
        for (i_, j_, state_, deltacost) in next(i,j,state):
            h.heappush(active, (cost + deltacost,i_,j_,state_))

print(f"part 1: {get_ans(1,4)}")
print(f"part 2: {get_ans(4,11)}")
