import numpy as np
from PIL import Image

inputf = 'test_input'
inputf = 'input'

nrg = []
### Read input data
with open(inputf, 'r') as fh:
    for line in fh:
        line = line.strip()
        b = list(line)
        nrg.append(b)

nrg = np.array(nrg, dtype=int)
nrg2 = nrg.copy()

### Part 1
def getMooreNeighbourIds(surface, y, x):

    height, width = surface.shape

    nids = []
    for ny in range(y-1, y+2):
        for nx in range(x-1, x+2):
            if ny == y and nx == x:
                continue
            if ( ny > -1 and ny < height and
                    nx > -1 and nx < width):
                nids.append([ny,nx])

    return nids

h,w = nrg.shape

ostate = np.zeros(nrg.shape, dtype=int)

def flash(y, x):
    global ostate
    global nrg

    # states
    # 0 - not flashed
    # flashed

    if ostate[y,x] == 1:
        return

    ostate[y,x] = 1

    # increase nrg of neighbours
    nb = getMooreNeighbourIds(nrg, y, x)

    # increment each of their nrgs
    for y,x in nb:
        nrg[y,x] += 1

    # call flash for each where necessary
    # where nrg > 9 and ostate == 0
    for y,x in nb:
        if nrg[y,x] > 9 and ostate[y,x] == 0:
            flash(y,x)


flashes = 0
for step in range(100):
    # reset state each iteration
    ostate = np.zeros(nrg.shape, dtype=int)

    # increase each nrg level
    for y in range(h):
        for x in range(w):
            nrg[y,x] += 1

    # check for flashes
    for y in range(h):
        for x in range(w):
            if nrg[y,x] > 9 and ostate[y,x] == 0:
                flash(y,x)

    # reset to 0 those that flashed (nrg>9)
    for y in range(h):
        for x in range(w):
            if nrg[y,x] > 9:
                nrg[y,x] = 0

    # count flashes
    flashes += np.sum(ostate)

    #print("\nAfter step", step, ":")
    #print(nrg)


print("Part1")
print("Number of flashes after 100 steps", flashes)

### Part 2
resmult = 8
im = Image.new('RGB', (h*resmult,w*resmult))

nrg = nrg2
flashes = 0
step = 0

while(True):
    pixellist = []
    # reset state each iteration
    ostate = np.zeros(nrg.shape, dtype=int)

    # increase each nrg level
    for y in range(h):
        for x in range(w):
            nrg[y,x] += 1

    # check for flashes
    for y in range(h):
        for x in range(w):
            if nrg[y,x] > 9 and ostate[y,x] == 0:
                flash(y,x)

    # make image
    for y in range(h):
        for mult in range(resmult):
            for x in range(w):
                nrglev = int(nrg[y,x]/9*180)
                for mult in range(resmult):
                    if nrg[y,x] > 9:
                        pixellist.append((255,255,255))
                    else:
                        pixellist.append((nrglev,nrglev,nrglev))

    # reset to 0 those that flashed (nrg>9)
    for y in range(h):
        for mult in range(resmult):
            for x in range(w):
                if nrg[y,x] > 9:
                    nrg[y,x] = 0

    im.putdata(pixellist)
    im.save("imgs/octopus_flashes_" + "0"*(3 - len(str(step))) + str(step) + ".png")

    step += 1

    # count flashes
    flashes = np.sum(ostate)
    if flashes == (w*h):
        break

print("Part 2")
print("Steps to synchronized flashes:", step)
