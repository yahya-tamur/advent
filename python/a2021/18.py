from common import get_problem
from collections import defaultdict

input = eval("[[[[[9,8],1],2],3],4]")

# node: something like [0,1,1]

# parse = eval!!

# things:

p = dict() # id -> id(parent)
l = dict() # id -> id(left)
r = dict() # id -> id(right)

val = dict() # id -> list. necessary?
current = 0

def visit(lst):
    global p, l, r, current

    # use current as id
    id = current
    val[id] = lst
    current += 1

    if type(lst) is list:
        l[id] = visit(lst[0])
        p[l[id]] = id

        r[id] = visit(lst[1])
        p[r[id]] = id
    else:
        l[id] = -1
        r[id] = -1

    return id

p[0] = -1
visit(input)

def explode():
    node = 0
    depth = 0
    def find(m, depth):
        if l[m] == -1:
            return -1
        if depth >= 4:
            return m
        if (v := find(l[m], depth+1)) != -1:
            return v
        return find(r[m], depth+1)
    exp = find(0,0)
    if exp == -1:
        return False
    # find prev node

    print(find(0, 0), val[find(0,0)])
    #node = input
    #depth = 0
    #fo

explode()
