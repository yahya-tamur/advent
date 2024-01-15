from problem import gp

def run(players, last):
    l = [0]
    r = [0]
    i = 0

    player = 0

    scores = {i: 0 for i in range(players)}

    for marble in range(1,last+1):
        player = (player + 1) % players
        if marble % 23 == 0:
            for _ in range(7):
                i = l[i]
            scores[player] += marble + i
            r[l[i]] = r[i]
            l[r[i]] = l[i]
            i = r[i]
            l.append(-1)
            r.append(-1)

        else:
            a, b = r[i], r[r[i]]

            r[a] = marble
            l[b] = marble
            l.append(a)
            r.append(b)

            i = marble
    return max(scores.values())

inp = gp().split(' ')
players, last = int(inp[0]), int(inp[6])

print(f"part 1: {run(players, last)}")
print(f"part 2: {run(players, 100*last)}")
