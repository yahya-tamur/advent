#heapremove turns out o be very inefficient since I was looking through
#the whole heap linearly to find the elements I wanted to remove.

#I also tried to keep a table of minimum costs per state but this is
#unnecessary since I process shortest paths first. We can just keep track of
# which states we've processed.

#I'll use complex numbers for directions next time.

from common import get_problem_lines
from math import inf
import heapq as h
from sys import exit
from time import time

map = [[int(c) for c in line] for line in get_problem_lines()]

#r, d, l, u = 0, 1, 2, 3

def get_ans(allowed_start, allowed_end):
    def next(i,j,state):
        ans = list()
        newstates = [0,1,2,3]
        if state != 0 and state != 2:
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
                    ans.append((i-r,j,2,dc))
        if state != 1 and state != 3:
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
                    ans.append((i,j-r,3,dc))
        return ans

    costs = [ [[inf for _ in range(4)] for _ in line] for line in map]
    costs[0][0][2] = 0
    costs[0][0][3] = 0
    active = [(0,0,0,2), (0,0,0,3)]

    prevs = dict()

    def heapremove(heap, i):
        #assertheap(heap)
        heap[i] = heap[-1]
        heap.pop()
        if i < len(heap):
            if i > 0 and heap[(i-1)//2] > heap[i]:
                while i > 0 and heap[(i-1)//2] > heap[i]:
                    heap[(i-1)//2], heap[i] = heap[i], heap[(i-1)//2]
                    i = (i-1)//2
            else:
                while True:
                    if len(heap) < i*2+2:
                        break
                    if len(heap) == i*2+2:
                        if heap[i] > heap[i*2+1]:
                            heap[i], heap[i*2+1] = heap[i*2+1], heap[i]
                        break
                    else:
                        next = i*2+1 if heap[i*2+1] < heap[i*2+2] else i*2+2
                        if heap[i] > heap[next]:
                            heap[i], heap[next] = heap[next], heap[i]
                            i = next
                        else:
                            break
        #assertheap(heap)

    def printstate():
        print('----'*150)
        for i in range(len(map)):
            for j in range(len(map[0])):
                m = min([costs[i][j][state] for state in range(4)])
                if m < inf:
                    m = '% 3d' % (m % 100)
                else:
                    m = 'fff'
                print(m, end='')
            print()
        print(len(active))


    lastprinted = time()
    def assertheap(heap):
        if not heap[0] == min(heap):
            print('ah')
            heap.sort()
            exit()
        for i in range(len(heap)):
            if not (2*i + 1 >= len(heap) or heap[i] <= heap[2*i+1]):
                print(i,2*i+1)
                print(heap)
                #print('ar')
                heap.sort()
                exit()
            if not (2*i + 2 >= len(heap) or heap[i] <= heap[2*i+2]):
                print(i,2*i+2)
                heap.sort()
                print('al')
                exit()

        
    prevs = dict()
    end = None
    ans = 0
    while True:
        #assertheap(active)
        _hscore, i, j, state = h.heappop(active)
        if time() - lastprinted > 2:
            printstate()
            lastprinted = time()
        if i == len(map)-1 and j == len(map[0])-1:
            ans = costs[i][j][state]
            end = (i,j, state)
            break
        for (i_, j_, state_, deltacost) in next(i,j,state):
            newcost = costs[i][j][state] + deltacost
            if newcost < costs[i_][j_][state_]:
                costs[i_][j_][state_] = newcost
                prevs[(i_,j_,state_)] = (i,j,state)
                #for k in range(len(active)):
                    #score__, i__, j__, state__ = active[k]
                    #if i_ == i__ and j_ == j__ and state__ == state_:
                        #heapremove(active, k)
                        #break
                h.heappush(active, (costs[i_][j_][state_],i_,j_,state_))

    #path = list()
    #path.append(end)
    #while prevs.get(path[-1]) is not None:
        #path.append(prevs[path[-1]])
    #path.reverse()

    #m = [['  .' for _ in line] for line in map]
    #for (n, (i,j,state)) in enumerate(path):
        #m[i][j] = '% 3d' % (n % 100)

    #for line in m:
        #for c in line:
            #print(c, end='')
        #print()
    return ans

print(f"part 1: {get_ans(1,4)}")
print(f"part 2: {get_ans(4,11)}")
