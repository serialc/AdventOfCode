import numpy as np
#from PIL import Image
#import re
#import sys

def matPrint(mat, sep=''):
    nh, nw = mat.shape
    print("Dimension", nh, nw)

    for y in range(nh):
        for x in range(nw):
            print(str(mat[y,x]) + sep, end='')
        print()

input_file = 'input0'
input_file = 'input'

uni = []
with open(input_file, 'r') as fh:
    for l in fh:
        l = l.strip('\n')

        if l == '':
            continue

        uni.append(list(l))

uni = np.array(uni)
uni_bu = uni # save for part2
#matPrint(uni)

# universe expansion - Vertical
exuni = None
for y in range(uni.shape[0]):
    if exuni is None:
        exuni = uni[y]
    else:
        exuni = np.vstack((exuni, uni[y]))

    if np.all(uni[y] == '.'):
        exuni = np.vstack((exuni, uni[y]))

# universe expansion - Horizontal
uni = exuni
exuni = None
for x in range(uni.shape[1]):
    if exuni is None:
        exuni = uni[:,x]
    else:
        exuni = np.vstack((exuni, uni[:,x]))

    if np.all(uni[:,x] == '.'):
        exuni = np.vstack((exuni, uni[:,x]))

# need to transpose exuni to return to correct orientation
exuni = exuni.transpose()
#matPrint(exuni)

galcount = np.sum(exuni == '#')
print("There are", galcount, "galaxies in this universe")

# get the coordinates of each galaxy
galcoords = np.where(exuni == '#')
gc = [(galcoords[0][i], galcoords[1][i]) for i in range(len(galcoords[0]))]

# calculate distances between galaxies
# save inter-galaxy distances
igd = []
for gi in range(len(gc)):
    for gi2 in range(gi+1, len(gc)):
        #print(gi,'-',gi2)
        y1, x1 = gc[gi]
        y2, x2 = gc[gi2]
        igd.append(abs(y2 - y1) + abs(x2 - x1))

print("#### Part 1 ####")
print("Answer is:", sum(igd))


#### PART 2 ####
print("============ Part 2 start ================")

# use the pre-expanded universe
uni = uni_bu

matPrint(uni)

# get the coordinates of each galaxy
galcoords = np.where(uni == '#')
gc = [(galcoords[0][i], galcoords[1][i]) for i in range(len(galcoords[0]))]

# identify which rows/cols are a million times larger
yexp = []
xexp = []
for y in range(uni.shape[0]):
    if np.all(uni[y] == '.'):
        yexp.append(y)
for x in range(uni.shape[1]):
    if np.all(uni[:,x] == '.'):
        xexp.append(x)

yexp = np.array(yexp)
xexp = np.array(xexp)

# calculate distances between galaxies
# save inter-galaxy distances
igd = []

for gi in range(len(gc)):
    for gi2 in range(gi+1, len(gc)):

        #print(gc[gi],'-',gc[gi2])
        y1, x1 = gc[gi]
        y2, x2 = gc[gi2]

        # count the number of expansions we cross
        expcnt = 0
        if y1 < y2:
            expcnt += np.sum(np.logical_and(yexp > y1, yexp < y2))
        if y1 > y2:
            expcnt += np.sum(np.logical_and(yexp < y1, yexp > y2))
        if x1 < x2:
            expcnt += np.sum(np.logical_and(xexp > x1, xexp < x2))
        if x1 > x2:
            expcnt += np.sum(np.logical_and(xexp < x1, xexp > x2))

        #print('expcnt',expcnt)
        # careful - need to multiply by x (1000000) but remove the pre-existing 1 value calculated
        igd.append(abs(y2 - y1) + abs(x2 - x1) + 1000000*expcnt - expcnt)

print("#### Part 2 ####")
print("Answer is:", sum(igd))
