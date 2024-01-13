from intcode import get_code, interact
from collections import defaultdict
import readline
from sys import exit, argv
import os

# I did have a lot of fun customizing the user interaction. I do like UI/UX design.


def play():
    intro = """
    This stage asks you to win a short text-based adventure game written
    in intcode. This is a simulation of the game with various quality of
    life improvements.

    Use the n, s, w, e shortcuts commands to move, the t shortcut command
    to pick up the first item.

    The map is also shown. Note that it's not perfect because there are
    several floors. For example, if it looks like there's a ladder between
    two rooms, one room definitely has a ladder there. The other room
    might have a wall, a door, or a ladder there.

    Another quality of life improvement is that many error messages will
    not overwrite what's written on the screen so you can usually still
    see the possible directions you can move to.

    I only tested this on a linux terminal -- one thing to change when using
    another terminal will be to use a different way of clearing the screen.

    Run 'python 25.py showans' to find the correct answer automatically.

    Press enter to get started.
    """

    os.system('clear')
    print(intro)
    input()





    resp, sv = interact(get_code())
    resp = ''.join((chr(c) for c in resp))
    comm = ""

    shortcuts = {'n': 'north', 'w': 'west', 'e': 'east', 's': 'south'}

    def sv_(comm):
        resp = list()
        for c in comm:
            if (dresp := sv(ord(c))) is not None:
                resp += dresp
            else:
                exit()
        return ''.join((chr(c) for c in resp))

    def draw_map():
        xs, ys = [z.real for z in map[height] if map[height][z]], [z.imag for z in map[height] if map[height][z]]
        x0, x1, y0, y1 = (int(u) for u in (min(xs), max(xs), min(ys), max(ys)))

        mmm = max((len(str(s)) for s in map[height].values()))+2

        ans = list()
        for i in range(x0,x1+2):
            mline, bline = ' ', ' '
            for j in range(y0, y1+2):
                z = i+1j*j
                if map[height][z-1j] or map[height][z]:
                    mline += '┃'
                else:
                    mline += ' '
                if z == loc:
                    mline += map[height][z]+'🯆 ' + (mmm - len(map[height][z])-2)*' ' 
                else:
                    mline += map[height][z] + (mmm - len(map[height][z]))*' ' 
                if map[height][z] or map[height][z-1]:
                    bline += '━'*(mmm+1)
                else:
                    bline += ' '*(mmm+1)
            ans.append(bline)
            ans.append(mline)

        h = lambda c: int(ans[c[0]][c[1]] == '━')
        v = lambda c: int(ans[c[0]][c[1]] == '┃')

        ans = [[' ' for c in ans[0]]] + [list(line) for line in ans]
        for i in range(1,len(ans)-1):
            for j in range(1,len(ans[0])-1):
                match (h((i,j-1)), h((i,j+1)), v((i-1,j)), v((i+1,j))):
                    case 1, 0, 1, 0:
                        ans[i][j] = '┛'
                    case 1, 0, 0, 1:
                        ans[i][j] = '┓'
                    case 0, 1, 1, 0:
                        ans[i][j] = '┗'
                    case 0, 1, 0, 1:
                        ans[i][j] = '┏'
                    case 1, 1, 1, 0:
                        ans[i][j] = '┻'
                    case 1, 1, 0, 1:
                        ans[i][j] = '┳'
                    case 1, 0, 1, 1:
                        ans[i][j] = '┫'
                    case 0, 1, 1, 1:
                        ans[i][j] = '┣'
                    case 1, 1, 1, 1:
                        ans[i][j] = '╋'

        for i in range(x0, x1+2):
            for j in range(y0, y1+2):
                ii = (i - x0)*2+2
                jj = (j - y0)*(mmm+1)+1
                z = i+1j*j
                if (z-1j, z) in doors[height]:
                    if doors[height][(z-1j,z)] == 1:
                        ans[ii][jj] = '?'
                    elif doors[height][(z-1j,z)] == 3:
                        ans[ii][jj] = ' '
                    else:
                        ans[ii][jj] = 'E'

                if (height, z-1j, z) in ladders:
                    ans[ii][jj] = '='
                ii -= 1
                jj += mmm // 2
                if (z-1, z) in doors[height]:
                    if doors[height][(z-1,z)] == 1:
                        ans[ii][jj] = '?'
                        ans[ii][jj+1] = '?'
                    elif doors[height][(z-1,z)] == 3:
                        ans[ii][jj] = ' '
                        ans[ii][jj+1] = ' '
                    else:
                        ans[ii][jj] = 'E'
                        ans[ii][jj+1] = 'E'
                if (height, z-1, z) in ladders:
                    ans[ii][jj] = 'H'
                    ans[ii][jj+1] = 'H'
                #ans[ii][jj] = str(j)[-1]


        ans = [''.join(line) for line in ans]

        for line in ans:
            print(line)



    map = [defaultdict(str)]
    height = 0

    doors = [defaultdict(int)]
    ladders = set()
    loc = 0
    prevloc = 0

    dirs = {'north\n': -1, 'south\n': 1, 'east\n': 1j, 'west\n': -1j}

    while comm != 'exit':

        resp = resp.strip() + '\n'

        unwanted = ["You can't go that way", 'Unrecognized command', 'You take', 'move!!', 'You drop', 'inventory', 'g any i']

        changed = False
        for u in unwanted:
            if u in resp:
                if any((u in message for u in unwanted)):
                    message = message[:message.find('Command')-1] +  resp
                else:
                    message = message[:message.find('Command')] +  resp
                changed = True

        if not changed:
            message = resp

        nomove = ["can't go that", "ejected back", "move!!", "entory", "g any i"]
        if comm in dirs and all((nm not in message for nm in nomove)):
            prevloc = loc
            loc += dirs[comm]

        if prevloc != loc:
            doors[height][(loc,prevloc)] |= 2
            doors[height][(prevloc,loc)] |= 2


        locname = message[message.rfind('= ')+1:message.rfind(' =')+1]

        prev_height = height
        if map[height][loc] != locname:
            existed = False
            for _height, layout in enumerate(map):
                if layout[loc] == locname:
                    height = _height
                    existed = True
                    break
            if not existed:
                if map[height][loc] != '':
                    map.append(defaultdict(str))
                    doors.append(defaultdict(int))
                    height = len(map)-1
                map[height][loc] = locname
        if height != prev_height:
            ladders.add((height, prevloc, loc))
            ladders.add((height, loc, prevloc))
            ladders.add((prev_height, prevloc, loc))
            ladders.add((prev_height, prevloc, prevloc))

        availocs = {dirs[dir] for dir in dirs if dir in message[message.rfind('here lead:\n'):]}
        for dir in availocs:
            doors[height][(loc,loc+dir)] |= 1
            doors[height][(loc+dir,loc)] |= 1

        os.system('clear')
        draw_map()


        print(message[:message.find('Command')-1])
        print(sv_('inv\n'))

        try:
            inp = input()
            if inp in shortcuts:
                inp = shortcuts[inp]
            if inp == 't':
                itms = message.find('Items here')
                l = message.find('- ', itms) + 2
                r = message.find('\n',l)
                inp = 'take ' + message[l:r]
            comm = inp + "\n"
        except KeyboardInterrupt:
            print()
            exit()
        resp = sv_(comm)

if 'play' in argv:
    play()

def win():

    def ppp(s):
        ans = ''
        for i in s:
            if i >= 0 and i < 256:
                ans += chr(i)
            else:
                ans += f"{{{i}}}"
        return ans

    display, sv = interact(get_code())
    display = ppp(display)

    def sv_(s):
        acc = list()
        for c in s + '\n':
            acc += sv(ord(c))
        return ppp(acc)

    def get_list(fro):
        l = display.rfind(fro)+len(fro)+3
        if l == len(fro)+2:
            return []
        r = display.find('\n\n',l)
        return display[l:r].split('\n- ')

    baditems = ['photons', 'giant electromagnet', 'escape pod', 'molten lava', 'infinite loop']

    opp = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
    seen = {'Security Checkpoint'}
    def exhaust():
        nonlocal display
        name = display[display.rfind('= ')+2:display.rfind(' =')]
        if name in seen:
            return
        seen.add(name)
        for dir in get_list('lead:'):
            display += sv_(dir)
            for item in get_list('here:'):
                if item not in baditems:
                    sv_(f'take {item}')
                exhaust()
            display += sv_(opp[dir])

    exhaust()
    display = sv_('inv')
    items = get_list('tory:')

    sv_('west\nsouth\nwest')

    #use a gray sequence here???
    athand = 0
    lll = len(items)
    for i in range(lll):
        sv_(f'drop {items[i]}')

    for i in range(2 ** lll):
        for j in range(lll):
            if i & (1 << j):
                sv_(f'take {items[j]}')

        mess = sv_('south')
        if 'Santa' in mess:
            if 'showans' in argv:
                print([items[j] for j in range(lll) if i & (1 << j)])
            l = mess.find('typing ')+7
            r = mess.find(' on')
            print(f"part 1: {mess[l:r]}")
            print(f"part 2: {'@'}")
            exit()

        for j in range(lll):
            if i & (1 << j):
                sv_(f'drop {items[j]}')

if 'play' not in argv:
    win()
