"""AoC 2025 Day 07."""

import numpy as np
import math
from PIL import Image

# import sys
# import time
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

    if mat.dtype == "float64" or mat.dtype == "int64":
        if value == "":
            value = 0
        nmat = np.full(np.array(mat.shape) + 2 * width, value, dtype=mat.dtype)

    # copy mat contents to new matrix
    nmat[width : mat.shape[0] + width, width : mat.shape[1] + width] = mat

    return nmat


input_file = "input0"
input_file = "input"

puz = []
with open(input_file, "r") as fh:
    step = 0
    for line in fh:
        line = line.strip("\n")

        puz.append(list(line))

# convert to numpy array
surf = np.array(puz)
# add border to make neighbourhood work on the edges more easily
# surf = matWrap(surf, value=".")

start = np.where(surf == "S")
# replace S with |
surf[start[0][0], start[1][0]] = "|"


scount = 0
for y in range(start[0][0], surf.shape[0] - 1):
    # get the beams on this line
    beams = np.where(surf[y, :] == "|")[0]

    # for each beam try and place beam below, unless splitter
    for beam in beams:
        if surf[y + 1, beam] == ".":
            surf[y + 1, beam] = "|"
        if surf[y + 1, beam] == "^":
            scount += 1
            surf[y + 1, beam - 1] = "|"
            surf[y + 1, beam + 1] = "|"


# matPrint(surf)

print("#### Part 1 ####")
print("Answer is:", scount)

# PART 2 ####
print("============ Part 2 start ================")

puz = []
with open(input_file, "r") as fh:
    step = 0
    for line in fh:
        line = line.strip("\n")

        puz.append(list(line))

# convert to numpy array
surf = np.array(puz)
# add border to make neighbourhood work on the edges more easily
# surf = matWrap(surf, value=".")

# make a matrix to hold counts
isurf = np.zeros(surf.shape, dtype=int)
# replace S with 1
start = np.where(surf == "S")
isurf[start[0][0], start[1][0]] = 1

for y in range(start[0][0], surf.shape[0] - 1):
    # get the beams on this line
    beams = np.where(isurf[y, :] != 0)[0]

    # for each beam try and place beam below, unless splitter
    for beam in beams:
        # below is a splitter
        if surf[y + 1, beam] == "^":
            # left
            isurf[y + 1, beam - 1] = isurf[y, beam] + isurf[y + 1, beam - 1]
            # right
            isurf[y + 1, beam + 1] = isurf[y, beam] + isurf[y + 1, beam + 1]
            continue

        # just add above to below
        isurf[y + 1, beam] += isurf[y, beam]

matPrint(isurf, cwidth=2)

# calculate the answer
cbeams = isurf[isurf.shape[0] - 1, :].sum()

print("#### Part 2 ####")
print("Answer is:", cbeams)

# make graphic
resmult = 3
# image size is (x,y) and not (y,x) like matrices!
im = Image.new("RGB", (isurf.shape[1] * resmult, isurf.shape[0] * resmult))
pixellist = []

max_val = math.log(isurf.max())
for y in range(isurf.shape[0]):
    for m in range(resmult):
        for x in range(isurf.shape[1]):
            v = int(isurf[y, x] / max_val * 765)
            v = int(math.log(isurf[y, x] + 1) / max_val * 200 + 55)
            for m2 in range(resmult):
                if surf[y, x] == "^":
                    pixellist.append((255, 0, 0))
                    continue
                if isurf[y, x] > 0:
                    # pixellist.append((0, 0, 255))
                    pixellist.append((v, v, v))
                    continue
                pixellist.append((0, 0, 0))

print("theoretical pixels", isurf.shape[0] * isurf.shape[1])
print("actual", len(pixellist))
im.putdata(pixellist)
im.save("pixel_density.png")
