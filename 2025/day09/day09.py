"""AoC 2025 Day 09."""

import sys
import numpy as np

# import math

# import time
# from PIL import Image
# import re


def matPrint(mat, cwidth=1, replace=0, replacement="."):
    """Print a matrix nicely."""
    nh, nw = mat.shape
    print("Dimension", nh, nw)

    for y in range(nh):
        for x in range(nw):
            vlen = len(str(mat[y, x]))
            if mat[y, x] == replace:
                print(replacement + " " * (cwidth - len(replacement)), end="")
            else:
                print(str(mat[y, x]) + " " * (cwidth - vlen), end="")
        print()


def matWrap(mat, width=1, value=""):
    """Add a border of values around a matrix."""
    h, w = mat.shape

    if mat.dtype == "U1":
        nmat = np.full(np.array(mat.shape) + 2 * width, value)

    vnumeric = ["float64", "int64", np.uint8]
    if mat.dtype in vnumeric:
        if value == "":
            value = 0
        nmat = np.full(np.array(mat.shape) + 2 * width, value, dtype=mat.dtype)

    # copy mat contents to new matrix
    nmat[width : mat.shape[0] + width, width : mat.shape[1] + width] = mat

    return nmat


# get input file from command line
input_file = "input"
if len(sys.argv) == 2:
    input_file += sys.argv[1]
print("\nProcessing input file:", input_file)

tloc = []
with open(input_file, "r") as fh:
    step = 0
    for line in fh:
        line = line.strip("\n")

        tloc.append([int(x) for x in line.split(",")])

ma = 0
for t1 in tloc:
    for t2 in tloc:
        area = abs(t1[0] - t2[0] + 1) * (t1[1] - t2[1] + 1)
        if area > ma:
            ma = area

print("#### Part 1 ####")
print("Answer is:", ma)

# PART 2 ###
print("\n============ Part 2 start ================")


sys.setrecursionlimit(100000)


def flood(surf, y, x, grp):
    """Flood contiguous areas with same group."""
    if surf[y, x] != 0:
        return

    surf[y, x] = grp

    h, w = surf.shape

    if x > 0:
        flood(surf, y, x - 1, grp)
    if x < (w - 1):
        flood(surf, y, x + 1, grp)
    if y > 0:
        flood(surf, y - 1, x, grp)
    if y < (h - 1):
        flood(surf, y + 1, x, grp)


# reform tloc to y,x form
tlocs = np.array(tloc)[:, [-1, -2]]

cornernum = tlocs.shape[0]
# area matrix (amat) needs to hold large ints ( e.g. 4 billion, needs 34 bits)
amat = np.zeros((cornernum, cornernum), dtype=np.uint64)

# calculate all possible rect areas
for t1i in range(cornernum):
    for t2i in range(cornernum):
        h = abs(tlocs[t1i, 0] - tlocs[t2i, 0]) + 1
        w = abs(tlocs[t1i, 1] - tlocs[t2i, 1]) + 1
        amat[t1i, t2i] = h * w

# print("Max area", np.max(amat))
# matPrint(amat, cwidth=3)

# compress the x,y coordinates into rank
# need to remove duplicates
tys = np.unique(tlocs[:, 0])
tys.sort()
txs = np.unique(tlocs[:, 1])
txs.sort()

rnkpos = np.zeros(tlocs.shape, dtype=np.int16)
for i in range(rnkpos.shape[0]):
    # find the rank of value
    ry = np.where(tys == tlocs[i, 0])[0][0]
    rx = np.where(txs == tlocs[i, 1])[0][0]
    # replace with rank
    rnkpos[i, :] = [ry, rx]

# create the surface and 'populate' it
surf = np.zeros((len(tys), len(txs)), dtype=np.uint8)

# matPrint(tlocs, 3)
# matPrint(rnkpos, 3)

for ti in range(cornernum):

    t1 = rnkpos[ti]
    # change to corner/red tile
    surf[t1[0], t1[1]] = 1

    # fill the tiles between this one and the next with Green/2 tiles
    tnxt = rnkpos[(ti + 1) % cornernum]

    # print("t1", t1, "tnxt", tnxt)

    # print("Pair of coords", t1, tnxt)
    ydiff = tnxt[0] - t1[0]
    xdiff = tnxt[1] - t1[1]

    # print("yx-diffs", ydiff, xdiff)

    if xdiff != 0:
        # draw horizontally
        # print("H")
        if xdiff > 0:
            # left to right
            for x in range(1, xdiff):
                surf[t1[0], t1[1] + x] = 2
        else:
            # right to left
            for x in range(1, abs(xdiff)):
                surf[tnxt[0], tnxt[1] + x] = 2

    if ydiff != 0:
        # draw vertically
        # print("V")
        if ydiff > 0:
            # down
            for y in range(1, ydiff):
                surf[t1[0] + y, t1[1]] = 2
        else:
            # up
            for y in range(1, abs(ydiff)):
                surf[tnxt[0] + y, tnxt[1]] = 2

# matPrint(surf)

# flood the outside areas
# add border so the flood can go around
wsurf = matWrap(surf, value=0)
# start flood in top-left corner
flood(wsurf, 0, 0, 4)
# reduce back to original size (and into surf)
surf = wsurf[1 : surf.shape[0] + 1, 1 : surf.shape[1] + 1]

# reassign to desired values
surf[surf == 0] = 2
surf[surf == 4] = 0

# now see if the rectangle between two points is valid
ma_bounds = []
maxarea = 0
for ti1 in range(cornernum):
    for ti2 in range(cornernum):
        # skip self
        if ti1 == ti2:
            continue

        area = amat[ti1, ti2]

        # get the ranked locations
        t1 = rnkpos[ti1, :]
        t2 = rnkpos[ti2, :]

        # print("Corners:", t1, t2, area)

        # for slicing need to select the positive range
        # from the top-left rectangle corner
        # is the x, y offset
        ydiff = t2[0] - t1[0]
        xdiff = t2[1] - t1[1]

        y = t1[0]
        x = t1[1]

        # print("old yx", y, x)
        # adjust x,y to have top-right corner coordinates
        if ydiff < 0:
            y += ydiff
        if xdiff < 0:
            x += xdiff

        # print("YX", y, x, "diffs", ydiff, xdiff)

        # before seeing if valid, is it even larger than our max area seen?
        if area > maxarea:
            # print("Slice", y, ":", abs(ydiff) + 1, ",", x, ":", x + abs(xdiff) + 1)
            # matPrint(surf[y : y + abs(ydiff) + 1, x : x + abs(xdiff) + 1])
            if np.all(surf[y : y + abs(ydiff) + 1, x : x + abs(xdiff) + 1] > 0):
                # print("Increased maxarea to", area)
                maxarea = area
                ma_bounds = (y, y + abs(ydiff) + 1, x, x + abs(xdiff) + 1)

matPrint(surf)

surf[ma_bounds[0] : ma_bounds[1], ma_bounds[2] : ma_bounds[3]] = 8

matPrint(surf)

print("#### Part 2 ####")
print("Answer is:", maxarea)
# 1452390036 - too low.
