import re
import numpy as np
import math

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

input_file = 'input_test'
input_file = 'input'

# create list of possible strings
tiles = {}
tdim = 10
with open(input_file, 'r') as fh:
    row = 0
    for line in fh:
        line = line.rstrip()

        if line == "":
            # add tile to list of tiles, create data structure to add info later
            tiles[tid] = {"map":tile[:], "neighbour":{}, "pos":[]} # deep copy
            continue

        tidmatch = re.match("Tile (\d+)\:", line)
        if tidmatch:
            tid = int(tidmatch.groups()[0])
            tile = []
            mode = 1
            continue

        # build tile
        tile.append(line)
        row += 1

# add last tile
tiles[tid] = {"map":[r[:] for r in tile], "neighbour":{}, "pos":[]} # deep copy
        
print("Found", len(tiles), "tiles.\n")

# augment the data so 

def getedge(tid, bearing):
    ''' Always returns edge in clockwise direction along edge '''

    # north
    if bearing == 0:
        return(tiles[tid]['map'][0])

    # east
    if bearing == 1:
        edge = ''
        for row in tiles[tid]['map']:
            edge += row[-1]
        return(edge)

    # south
    if bearing == 2:
        return(tiles[tid]['map'][-1][::-1])

    # east
    if bearing == 3:
        edge = ''
        for row in tiles[tid]['map']:
            edge += row[0]
        return(edge[::-1])

def fliptile(tid):
    newtile = []
    for row in tiles[tid]['map']:
        newtile.insert(0,row)
    tiles[tid]['map'] = newtile

def rotatetile(tid):
    tiles[tid]['map'] = ["".join(row) for row in list(zip(*tiles[tid]['map'][::-1]))]

def showtile(tid):
    print("Tile", tid)
    for tilerow in tiles[tid]['map']:
        for i in tilerow:
            if i == '#':
                print(bcolors.OKGREEN + str(i) + bcolors.ENDC, end='')
            elif i == 'O':
                print(bcolors.FAIL + str(i) + bcolors.ENDC, end='')
            else:
                print(bcolors.OKBLUE + str(i) + bcolors.ENDC, end='')
        print()
    print()

def showarrangement():
    wh = int(math.sqrt(len(tiles)))

    # get the number of min of x,y positions
    minx = wh
    miny = wh
    tilelocdict = {}
    for tid in tiles:
        # if has coordinates defined
        if len(tiles[tid]['pos']) == 2:
            x = tiles[tid]['pos'][0]
            y = tiles[tid]['pos'][1]

            tilelocdict[str(x) + '_' + str(y)] = tid

            if x < minx:
                minx = x
            if y < miny:
                miny = y

    corner_product = 1
    tilemap = []
    for y in range(miny, miny + wh):
        tilemap.append([])
        for x in range(minx, minx + wh):
            key = str(x) + '_' + str(y)
            if key in tilelocdict:
                print(str(tilelocdict[key]) + ' ', end='')
                tilemap[len(tilemap)-1].append(tilelocdict[key])
            else:
                print(" "*4 + ' ', end='')

            # calc corner product
            if  (x == minx and y == miny) or \
                (x == minx and y == (miny + wh - 1)) or \
                (x == (minx + wh - 1) and y == miny) or \
                (x == (minx + wh - 1) and y == (miny + wh - 1)):
                corner_product *= tilelocdict[key]
        print()

    #print(tilelocdict)
    return(corner_product, tilemap)


def showtiles():
    for tid in tiles:
        showtile(tid)

def match_tile(ftid, fbearing, fedge, mtid):
    ''' check if matchtile shares and edge with fixedtile
        if so flip and rotate as needed matchtile '''

    rfedge = fedge[::-1]
    for mbearing in range(4):
        medge = getedge(mtid, mbearing)
        if rfedge == medge:
            fliptile(mtid) # top to bottom
            #print("Flipped", mtid)
            matched = match_tile(ftid, fbearing, fedge, mtid)
            if matched:
                return True
            else:
                exit("This should never happen as we found a match then flipped it!")

        if fedge == medge:
            # save to the fixed tile which tile matches to which bearing
            tiles[ftid]['neighbour'][fbearing] = mtid

            # rotate the matching tile 
            while fbearing != (mbearing + 2)%4:
                mbearing += 1
                rotatetile(mtid)

            # give the matched tile its location
            pos = tiles[ftid]['pos'][:]
            if fbearing == 0:
                pos[1] -= 1
            if fbearing == 1:
                pos[0] += 1
            if fbearing == 2:
                pos[1] += 1
            if fbearing == 3:
                pos[0] -= 1

            tiles[mtid]['pos'] = pos

            #print("Fixed", ftid, "bearing", fbearing, "to matched", mtid, "bearing",mbearing)
            return True

# work with the assumption that the first tile is in the correct position [0,0]
# build on it. 

def find_adjacent_tiles(tid):
    global processed_tiles
    if tid in processed_tiles:
        return

    processed_tiles.append(tid)

    #print("FAT", tid)

    # find match for each edge
    for fbearing in range(4):
        # get the edge and reversed
        fedge = getedge(tid, fbearing)[::-1]

        # look through all other tiles for matching edge
        for mtid in tiles:
            # skip yourself
            if tid == mtid:
                continue

            # this solves the location of the neighbours
            if match_tile(tid, fbearing, fedge, mtid):
                # matched
                break


        if fbearing in tiles[tid]['neighbour'] and tiles[tid]['neighbour'][fbearing] is None:
            continue
        if fbearing not in tiles[tid]['neighbour']:
            # this is an edge piece
            tiles[tid]['neighbour'][fbearing] = None
        else:
            # neighbour id
            nid = tiles[tid]['neighbour'][fbearing]

            # recursion
            find_adjacent_tiles(nid)
            pass

    #print(tid, tiles[tid]['neighbour'])


startid = list(tiles.keys())[0]
tiles[startid]['pos'] = [0,0]
processed_tiles = []

find_adjacent_tiles(startid)

#showtiles()

# multiply ids of corner tiles together
cproduct, tilemap = showarrangement()
print("Part 1 - Corner tile id product is", cproduct, "\n\n")

# crop each tile
# merge tiles into one 'image'
img = []

# get each row of tiles
for tidrow in tilemap:
    # trim the number of rows within tiles
    for rn in range(1, tdim - 1):
        rowdata = ''
        # append each tile's data to the img
        for tid in tidrow:
            rowdata += tiles[tid]['map'][rn][1:(tdim-1)]
        img.append(rowdata)

# so we can apply the functions
tiles['img'] = {"map":img}

# to match test case
#fliptile('img')
#rotatetile('img')
#showtile('img')

# load sea monster, only hash symbols need to match
seamonster =\
'''                  # 
#    ##    ##    ###
 #  #  #  #  #  #   '''

sm = []
smw = None
smh = None
for line in seamonster.split('\n'):
    sm.append([i for i in range(len(line)) if line[i] == '#'])
    if smw is None:
        smw = max(sm[-1])
    if smw < max(sm[-1]):
        smw = max(sm[-1])
smh = len(sm)


#print("Sea monster",sm, "w:", smw, "h:", smh, "\n\n")

def smwrite(x,y):
    #print("Found Sea Monster at x",x,"y",y)
    for smrow in range(len(sm)):
        for smcol in sm[smrow]:
            clist = list(tiles['img']['map'][smrow+y])
            clist[smcol+x] = 'O'
            tiles['img']['map'][smrow+y] = "".join(clist)

def smsearch(x,y):
    for smrow in range(len(sm)):
        for smcol in sm[smrow]:
            if tiles['img']['map'][smrow+y][smcol+x] != '#':
                return False
    smwrite(x,y)
    return True

# Need to scan image for all possible rotations and mirrored/flip

def scan_for_sea_monster():
    mapdim = len(tiles['img']['map'])
    smcount   = 0

    for row in range(mapdim - smh):
        # check if seamonster could be here or farther to the right
        for col in range(mapdim - smw):
            if smsearch(col,row):
                smcount += 1

    hashcount = 0
    for row in range(mapdim):
        hashcount += sum([1 for c in tiles['img']['map'][row] if c == '#'])

    if smcount > 0:
        showtile('img')
        print("Hash total", hashcount)
        print("SeaMonster total", smcount)
        return True
    else:
        print("Found no SeaMonster")
        return False

found = False
for mirror in range(2):
    for bearing in range(4):
        print("Scanning in bearing", bearing, "and mirrored", mirror)
        if scan_for_sea_monster():
            found = True
            break
        rotatetile('img')
    if found:
        break
    fliptile('img')

from PIL import Image
mapdim = len(tiles['img']['map'])
im = Image.new('RGB', (mapdim*2, mapdim*2))
pixellist = []
col_froth = (0,150,200)
col_water = (0,105,148)
col_monster = (255,100,100)
for row in tiles['img']['map']:
    # double pixel height
    for j in range(2):
        for c in row:
            # double pixel length
            for i in range(2):
                if c == '.':
                    pixellist.append(col_water)
                if c == '#':
                    pixellist.append(col_froth)
                if c == 'O':
                    pixellist.append(col_monster)
im.putdata(pixellist)
im.save('seamonsters.png')

