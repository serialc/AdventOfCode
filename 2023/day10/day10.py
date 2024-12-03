import numpy as np
from PIL import Image
#import re
import sys


def matPrint(mat, sep=''):
    nh, nw = mat.shape
    print("Dimension", nh, nw)

    for y in range(nh):
        for x in range(nw):
            print(str(mat[y,x]) + sep, end='')
        print()

input_file = 'input0'
input_file = 'input'

pmap = []
with open(input_file, 'r') as fh:
    for l in fh:
        l = l.strip('\n')

        if l == '':
            continue

        pmap.append(list(l))

# convert from list to np.array
pmap = np.array(pmap)
start = np.where(pmap == 'S')
start = [start[0][0], start[1][0]]

#print('start coords:', start)
#matPrint(pmap)

# overwrite start with correct symbol
#pmap[start[0]][start[1]] = 'F'
pmap[start[0]][start[1]] = 'J'

# create routing map
smap = np.zeros([len(pmap), len(pmap[0])], dtype=int)

def route(y, x, d, scorch=False):
    smap[y, x] = d

    # which directions does my pipe go?
    # will only go one way
    if pmap[y][x] == '|':
        if smap[y-1, x] == 0:
            # going up
            if scorch:
                if rmap[y, x+1] == ' ':
                    rmap[y, x+1] = 'R'
                if rmap[y, x-1] == ' ':
                    rmap[y, x-1] = 'L'
            route(y-1, x, d+1, scorch)
        if smap[y+1, x] == 0:
            # going down
            if scorch:
                if rmap[y, x+1] == ' ':
                    rmap[y, x+1] = 'L'
                if rmap[y, x-1] == ' ':
                    rmap[y, x-1] = 'R'
            route(y+1, x, d+1, scorch)

    if pmap[y][x] == '-':
        if smap[y, x+1] == 0:
            # going right
            if scorch:
                if rmap[y+1, x] == ' ':
                    rmap[y+1, x] = 'R'
                if rmap[y-1, x] == ' ':
                    rmap[y-1, x] = 'L'
            route(y, x+1, d+1, scorch)
        if smap[y, x-1] == 0:
            # going left 
            if scorch:
                if rmap[y+1, x] == ' ':
                    rmap[y+1, x] = 'L'
                if rmap[y-1, x] == ' ':
                    rmap[y-1, x] = 'R'
            route(y, x-1, d+1, scorch)

    if pmap[y][x] == 'L':
        if smap[y-1, x] == 0:
            # going up
            if scorch:
                if rmap[y, x-1] == ' ':
                    rmap[y, x-1] = 'L'
                if rmap[y+1, x] == ' ':
                    rmap[y+1, x] = 'L'
            route(y-1, x, d+1, scorch)
        if smap[y, x+1] == 0:
            # going right
            if scorch:
                if rmap[y, x-1] == ' ':
                    rmap[y, x-1] = 'R'
                if rmap[y+1, x] == ' ':
                    rmap[y+1, x] = 'R'
            route(y, x+1, d+1, scorch)

    if pmap[y][x] == 'J':
        if smap[y-1, x] == 0:
            # going up
            if scorch:
                if rmap[y+1, x] == ' ':
                    rmap[y+1, x] = 'R'
                if rmap[y, x+1] == ' ':
                    rmap[y, x+1] = 'R'
            route(y-1, x, d+1, scorch)
        if smap[y, x-1] == 0:
            # going left
            if scorch:
                if rmap[y+1, x] == ' ':
                    rmap[y+1, x] = 'L'
                if rmap[y, x+1] == ' ':
                    rmap[y, x+1] = 'L'
            route(y, x-1, d+1, scorch)

    if pmap[y][x] == '7':
        if smap[y+1, x] == 0:
            # going down
            if scorch:
                if rmap[y, x+1] == ' ':
                    rmap[y, x+1] = 'L'
                if rmap[y-1, x] == ' ':
                    rmap[y-1, x] = 'L'
            route(y+1, x, d+1, scorch)
        if smap[y, x-1] == 0:
            # going left
            if scorch:
                if rmap[y, x+1] == ' ':
                    rmap[y, x+1] = 'R'
                if rmap[y-1, x] == ' ':
                    rmap[y-1, x] = 'R'
            route(y, x-1, d+1, scorch)

    if pmap[y][x] == 'F':
        if smap[y, x+1] == 0:
            # going right
            if scorch:
                if rmap[y-1, x] == ' ':
                    rmap[y-1, x] = 'L'
                if rmap[y, x-1] == ' ':
                    rmap[y, x-1] = 'L'
            route(y, x+1, d+1, scorch)
        if smap[y+1, x] == 0:
            # going down
            if scorch:
                if rmap[y-1, x] == ' ':
                    rmap[y-1, x] = 'R'
                if rmap[y, x-1] == ' ':
                    rmap[y, x-1] = 'R'
            route(y+1, x, d+1, scorch)

#print(sys.getrecursionlimit())
sys.setrecursionlimit(20000)
# start at 1 rather then 0
route(start[0], start[1], 1)

# convert all values > 0 to 1 for viewing
#matPrint((smap > 0) * 1)

print("#### Part 1 ####")
print("Answer is:", smap.max()/2)


#### PART 2 ####
print("============ Part 2 start ================")

rmap = np.zeros(smap.shape, dtype='str_')
rmap.fill(' ')
rmap[smap>0] = '.'
# go through maze again - this time marking any smap free (0) spots
# as either left 'L' or right 'R' of the direction of travel

# erase smap
smap = np.zeros([len(pmap), len(pmap[0])], dtype=int)
# provide heading
route(start[0], start[1], 1, True)

# see map in symbols 
#symmap = pmap
#symmap[smap == 0] = ' '
#matPrint(symmap)
resmult = 8
im = Image.new('RGB', (rmap.shape[0]*resmult, rmap.shape[1]*resmult))

# copy for animation, slows processing
rmap2 = rmap.copy()
# flood space based on adjacency
steps = 0
while True:
    expansion = 0
    for y in range(rmap.shape[0]):
        for x in range(rmap.shape[1]):
            if rmap[y,x] == ' ':
                if y > 0 and rmap[y-1,x] != ' ':
                    rmap2[y,x] = rmap[y-1,x]
                    expansion += 1
                if y < (rmap.shape[0] - 1) and rmap[y+1,x] != ' ':
                    rmap2[y,x] = rmap[y+1,x]
                    expansion += 1
                if x > 0 and rmap[y,x-1] != ' ':
                    rmap2[y,x] = rmap[y,x-1]
                    expansion += 1
                if x < (rmap.shape[1] - 1) and rmap[y,x+1] != ' ':
                    rmap2[y,x] = rmap[y,x+1]
                    expansion += 1

    rmap = rmap2.copy()

    # make image
    pixellist = []
    for y in range(rmap.shape[0]):
        for mult in range(resmult):
            for x in range(rmap.shape[1]):
                col = (0,0,0)
                if rmap[y,x] == '.':
                    col = (255,255,255)
                if rmap[y,x] == 'L':
                    col = (255,128,128)
                if rmap[y,x] == 'R':
                    col = (128,255,128)

                for mult in range(resmult):
                    pixellist.append(col)

    im.putdata(pixellist)
    im.save("imgs/flood_" + "0"*(3 - len(str(steps))) + str(steps) + ".png")

    steps += 1
    if expansion == 0:
        break

matPrint(rmap)

print("#### Part 2 ####")
print("Answer is:", np.sum(rmap == 'R'))
