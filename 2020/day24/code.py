import re
import numpy as np
#import math
#import time
from PIL import Image

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
#input_file = 'input_test2'
input_file = 'input'

inst = []
with open(input_file, 'r') as fh:
    for line in fh:
        line = line.rstrip()
        if line == "":
            break

        tins = []
        while len(line) > 0:
            dm = re.match("(e|se|sw|w|nw|ne)", line)
            val = dm.groups()[0]
            tins.append(val)
            line = line[len(val):]
        inst.append(tins)

maxin = max([len(i) for i in inst])
maxin = 75

print("Number of instructions is", len(inst))
print("Longest instruction is",max([len(i) for i in inst]),"steps.")

hsp = np.zeros(2*maxin * 2*maxin, dtype=int).reshape(2*maxin,2*maxin)


imgnum = 1
def hprint(hgrid):
    global imgnum

    # saving as image stuff
    mapdim = len(hgrid) + 1
    im = Image.new('RGB', (mapdim, mapdim))
    pixellist = []

    # display/add to image
    for row in range(len(hgrid)-1,-1,-1):
        if row%2 == 1:
            print(" ", end='')
            pixellist.append((255,255,255))
        for i in range(len(hgrid[row])):
            v = hgrid[row][i]
            if row == maxin and i == maxin:
                # centre tile/red
                print("" + bcolors.FAIL + str(v) + bcolors.ENDC, end='')
                pixellist.append((184,53,45))
                continue
            if v == 1:
                # black
                print("" + bcolors.OKGREEN + str(v) + bcolors.ENDC, end='')
                pixellist.append((0,0,0))
            else:
                # white
                print("" + str(v), end='')
                pixellist.append((255,255,255))
        if row%2 == 0:
            print(" ", end='')
            pixellist.append((255,255,255))
        print()
    print()

    # saving as image stuff
    im.putdata(pixellist)
    im.save("imgs/hextiles_" + "0"*(3 - len(str(imgnum))) + str(imgnum) + ".png")
    imgnum += 1

# set initial state
# for each instruction set
for hit in inst:
    x = maxin
    y = maxin
    # for each direction
    for d in hit:
        if d == 'e':
            x += 1
            continue
        if d == 'w':
            x -= 1
            continue

        if y%2 == 1:
            if d == 'ne':
                y += 1 
                x += 1
            if d == 'nw':
                y += 1 

            if d == 'se':
                y -= 1 
                x += 1
            if d == 'sw':
                y -= 1 

        else:
            if d == 'ne':
                y += 1 
            if d == 'nw':
                y += 1 
                x -= 1

            if d == 'se':
                y -= 1 
            if d == 'sw':
                y -= 1 
                x -= 1

    #print("Instructions [" + " ".join(hit) + "] is flipping x,y=[" + str(x) + "," + str(y) + "]")
    if hsp[y][x] == 1:
        hsp[y][x] = 0
    else:
        hsp[y][x] = 1

hprint(hsp)
print("Number of black tiles is ",np.sum(hsp))

def hexproxsum(hs,x,y):
    nsum = 0
    nsum += hs[y][x+1] # e
    nsum += hs[y][x-1] # w

    if y%2 == 1:
        nsum += hs[y+1][x+1] # ne
        nsum += hs[y+1][x] # nw
        nsum += hs[y-1][x+1] # se
        nsum += hs[y-1][x] # sw

    else:
        nsum += hs[y+1][x] # ne
        nsum += hs[y+1][x-1] # nw
        nsum += hs[y-1][x] # se
        nsum += hs[y-1][x-1] # sw
    return(nsum)

def hexca(hexsurf):
    nhs = hexsurf.copy()
    # get each row - skip first/last row
    for r in range(1,len(hexsurf)-1):
        # get each item in row - skip first/last item
        for c in range(1,len(hexsurf[r])-1):
            hps = hexproxsum(hexsurf,c,r)

            if hexsurf[r][c] == 1 and hps == 0 or hps > 2:
                nhs[r][c] = 0 # make it white
            if hexsurf[r][c] == 0 and hps == 2:
                nhs[r][c] = 1 # make it black
            # otherwise stays the same
    return nhs

for dayint in range(100):
    hsp = hexca(hsp)
    hprint(hsp)

print("Number of black tiles is ",np.sum(hsp))
