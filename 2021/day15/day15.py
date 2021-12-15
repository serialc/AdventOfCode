import numpy as np
#import time
#from PIL import Image
import sys

print("Recursion limit", sys.getrecursionlimit())

inputf = 'test_input'
inputf = 'input'

def matPrint(mat, sep=''):
    nh,nw = mat.shape
    for y in range(nh):
        for x in range(nw):
            print(str(mat[y,x]) + sep, end='')
        print()

### Read input data
cmap = []
with open(inputf, 'r', encoding='utf-8-sig') as fh:
    for line in fh:
        line = line.strip()
        cmap.append(list(line))

cmap = np.array(cmap, dtype=int)

def getVonNeumannNeighboursId(surface, risk, y,x):

    height,width = surface.shape
    n = []

    if y != 0:
        n.append([y-1, x, surface[y-1, x], risk[y-1, x]])
    if x != 0:
        n.append([y, x-1, surface[y, x-1], risk[y, x-1]])
    if y != (height-1):
        n.append([y+1, x, surface[y+1, x], risk[y+1, x]])
    if x != (width-1):
        n.append([y, x+1, surface[y, x+1], risk[y, x+1]])

    return np.array(n, dtype=int)


def solveRiskMap(cmap):
    h,w = cmap.shape
    comp = np.zeros(cmap.shape, dtype=int)
    comp[0,0] = 1
    rmap = np.zeros(cmap.shape, dtype=int)

    # create cost surface to solve
    unsolved = True
    while unsolved:
        unsolved = False

        # process entire matrix
        for y in range(h):
            for x in range(w):

                # get computed neighbour ids
                n = getVonNeumannNeighboursId(comp, rmap, y, x)

                # get the total risk values of the neighbours
                adjacent_completed_risk_values = [nr for ny,nx,nc,nr in n if nc == 1]

                # if we have no adjacent cells that already processed a risk value, continue
                if len(adjacent_completed_risk_values) == 0:
                    continue

                # we have the lowest adjacent risk value
                min_rv = np.min(adjacent_completed_risk_values)

                # check each neighbour to find out which it is (the min_rv)
                for ny, nx, nc, nr in n:
                    # if it's completed (nc == 1) and it is the lowest risk (rmap)
                    if nc == 1 and nr == min_rv:
                        # if this point already has a risk, but that risk is higher than our neighbour value + my base risk
                        if comp[y,x] == 0 or (comp[y,x] == 1 and rmap[y,x] > (min_rv + cmap[y,x])):
                            rmap[y,x] = cmap[y,x] + min_rv
                            comp[y,x] = 1
                            unsolved = True
                            break

    return rmap

### Part 1
rmap = solveRiskMap(cmap)
h,w = rmap.shape
print("Part 1 answer", rmap[h-1,w-1])

### Part 2
print("=========== PART 2 ===============")

# increase size of cave map (cmap)
mult = 5
cave = cmap.copy()
tile = cmap.copy()
for xm in range(1, mult):
    tile += 1
    tile[tile == 10] = 1
    cave = np.concatenate((cave, tile), axis=1)

lcave = cave.copy()
xtile = cave.copy()

for ym in range(1, mult):
    xtile += 1
    xtile[xtile == 10] = 1
    lcave = np.concatenate((lcave, xtile), axis=0)

rmap = solveRiskMap(lcave)
h,w = rmap.shape
print("Part 2 answer", rmap[h-1,w-1])

#### Bonus ####
print("=========== BONUS ===============")
print("Finding the shortest route")

solpath = np.zeros(rmap.shape, dtype=int)

def findStart(y,x,d):
    if solpath[y,x] == 1:
        return

    solpath[y,x] = 1

    if x == 0 and y == 0:
        print("depth", d)
        return

    if (d + 100) > sys.getrecursionlimit():
        sys.setrecursionlimit(sys.getrecursionlimit() + 100)
        print("Increasing recursion limit to", sys.getrecursionlimit())

    # what was the total risk of the cell we came from
    source_total_risk = rmap[y,x] - lcave[y,x]

    # get neighbours
    n = getVonNeumannNeighboursId(solpath, rmap, y, x)

    # get the cell y,x that has the same source_total_risk
    # can return multiple cells, as there are multiple possible routes
    poss_sources = [[ny,nx,nr] for ny,nx,ns,nr in n if nr == source_total_risk]

    for ps in poss_sources:
        ny, nx, nr = ps
        findStart(ny,nx,d+1)

    return 

findStart(w-1,h-1,0)
#matPrint(solpath)

print("Generating image")

from PIL import Image

imgmin = 500
magnification = 1
while (w * magnification) < imgmin:
    magnification *= 2

im = Image.new('RGB', (w*magnification,h*magnification))
pixellist = []
for y in range(h):
    for i in range(magnification):
        for x in range(w):
            for i in range(magnification):
                elev = int(lcave[y,x]/9*128)
                if solpath[y,x] == 1:
                    pixellist.append((128 + elev,elev,elev))
                else:
                    pixellist.append((elev,elev,128 + elev))

im.putdata(pixellist)
im.save('cave_risk_' + inputf + '.png')
