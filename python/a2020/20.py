from problem import gp
from collections import defaultdict

def get_signatures(tile):
    strs = [tile[:tile.find('\n')], tile[tile.rfind('\n'):], "", ""]
    for line in tile.split('\n'):
        strs[2] += line[0]
        strs[3] += line[-1]
    strs += [s[::-1] for s in strs]
    return [int(s.replace('#','1').replace('.','0'),base=2) for s in strs]

signatures = defaultdict(int) # (base 2 int -> tile num)
graph = dict()
tiles = dict()

for tile in gp().split('\n\n'):
    if not tile:
        continue
    (title, _, tile) = tile.partition('\n')
    title = int(title[title.find(' ')+1:title.find(':')])
    tiles[title] = [list(l) for l in tile.split('\n')]
    graph[title] = set()
    for s in get_signatures(tile):
        if s in signatures:
            graph[title].add(signatures[s])
            graph[signatures[s]].add(title)
        else:
            signatures[s] = title

corners = [title for title, edges in graph.items() if len(edges) == 2]
print(f"part 1: {corners[0]*corners[1]*corners[2]*corners[3]}")

# I build the tileset from 'graph', trying every orientation, instead of
# calculating along with signatures. Redundant, but it worked first try!!!

def rotate(tile):
    return [[tile[j][~i] for j in range(len(tile))] for i in range(len(tile))]

def flip(tile):
    return [[tile[~i][j] for j in range(len(tile))] for i in range(len(tile))]

# returns correctly oriented tile or None
# left=True: stitches left. False: stitches down.
def stitch(left, anchor, tile):
    for _dir in range(4):
        tile = rotate(tile)
        for _flip in range(2):
            tile = flip(tile)
            if left and all((anchor[j][-1] == tile[j][0] for j in range(len(tile)))):
                return tile
            if (not left) and \
                    all((anchor[-1][j] == tile[0][j] for j in range(len(tile)))):
                return tile
    return None

def extend(index, tile, left): # left same as stitch
    for index_ in graph[index]:
        if (tile_ := stitch(left, tile, tiles[index_])) is not None:
            return [(index, tile)] + extend(index_, tile_, left)
    return [(index, tile)]

def get_topleft():
    tile = tiles[corners[0]]
    a, b = graph[corners[0]]
    for _dir in range(4):
        tile = rotate(tile)
        for _flip in range(2):
            tile = flip(tile)
            for _ns in range(2):
                a, b = b, a
                if stitch(True, tile, tiles[a]) and stitch(False, tile, tiles[b]):
                    return corners[0], tile

tileset = [[tile_ for _, tile_ in extend(index, tile, True)] \
        for index, tile in extend(*get_topleft(), False)]

n, m, ts = len(tileset), len(tileset[0]), len(tileset[0][0])

map = \
    [ \
        [ \
            tileset[tilerow][tilecol][row][col] \
            for tilecol in range(m) for col in range(1,ts-1) \
        ] \
        for tilerow in range(n) for row in range(1,ts-1) \
    ]

mon = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """[1:]

mon = [(i, j) for i, line in enumerate(mon.split('\n')) \
        for j, c in enumerate(line) if c == '#']

# non overlapping monsters
for _dir in range(4):
    map = rotate(map)
    for _flip in range(2):
        map = flip(map)
        for n in range(len(map)):
            for m in range(len(map)):
                if all((n+i < len(map) and m+j < len(map[0]) and \
                        map[n+i][m+j] == '#' for i, j in mon)):
                    for i, j in mon:
                        map[n+i][m+j] = '.'

hts = {(i, j) for i, line in enumerate(map) \
        for j, c in enumerate(line) if c == '#'}

print(f"part 2: {sum((1 for line in map for c in line if c == '#'))}")

