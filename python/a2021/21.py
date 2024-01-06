from problem import get_problem_lines
start = [ int(line.split(':')[1]) - 1 for line in get_problem_lines() ]
# player = [3, 7]

player = [start[0], start[1]]
scores = [0,0]

die = 1
rolled = 0

def get_die():
    global die, rolled
    rolled += 1
    ans = die
    die += 1
    if die == 101:
        die = 1
    return ans


while True:
#for _ in range(3):
    player[0] = (player[0] + get_die() + get_die() + get_die()) % 10
    scores[0] += player[0] + 1
    if scores[0] >= 1000:
        break
    player[1] = (player[1] + get_die() + get_die() + get_die()) % 10
    scores[1] += player[1] + 1
    if scores[1] >= 1000:
        break

    if scores[0] >= 1000:
        break

print(f"part 1: {min(scores)*rolled}")

dice_dist = [i+j+k for i in range(1,4) for j in range(1,4) for k in range(1,4)]
dice_dist = [(i,len([d for d in dice_dist if d == i])) for i in range(3,10)]

# max number of states: 10*10*21*21*2 : manageable
states = dict() # (p1, p2, s1, s2,turn) -> [p1win, p2win]
def get_wins(p1, p2, s1, s2, turn):
    if s1 >= 21:
        return [1,0]
    if s2 >= 21:
        return [0,1]
    if (wl := states.get((p1,p2,s1,s2,turn))) is not None:
        return wl
    w, l = 0, 0
    for (num, unvs) in dice_dist:
        if turn == 1:
            p1_ = (p1 + num) % 10
            (w_,l_) = get_wins(p1_, p2, s1 + p1_ + 1, s2, 2)
            w += w_*unvs
            l += l_*unvs
        else:
            p2_ = (p2 + num) % 10
            (w_,l_) = get_wins(p1, p2_, s1, s2 + p2_ + 1, 1)
            w += w_*unvs
            l += l_*unvs
    states[(p1,p2,s1,s2,turn)] = (w,l)
    return (w,l)

print(f"part 2: {max(get_wins(start[0],start[1],0,0,1))}")
