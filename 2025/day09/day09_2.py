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

    if mat.dtype == "float64" or mat.dtype == "int64":
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


tlocs = np.array(tloc)

# make the surface
maxx, maxy = np.max(tlocs, axis=0)

# look for duplicates

# set type to smaller so we can do this
surf = np.zeros((maxy + 2, maxx + 2), dtype=np.uint8)
print("Surface shape is", surf.shape)

tnum = len(tloc)
for ti in range(tnum):
    t1 = tloc[ti]
    surf[t1[1], t1[0]] = 1

    # fill the tiles between this one and the next with Green/2 tiles
    tnxt = tloc[(ti + 1) % tnum]

    # print("Pair of coords", t1, tnxt)
    xdiff = tnxt[0] - t1[0]
    ydiff = tnxt[1] - t1[1]

    if xdiff != 0:
        if xdiff > 0:
            for x in range(1, xdiff):
                surf[t1[1], t1[0] + x] = 2
        else:
            for x in range(1, abs(xdiff)):
                surf[t1[1], t1[0] - x] = 2

    if ydiff != 0:
        if ydiff > 0:
            for y in range(1, ydiff):
                surf[t1[1] + y, t1[0]] = 2
        else:
            for y in range(1, abs(ydiff)):
                surf[t1[1] - y, t1[0]] = 2


# sys.setrecursionlimit(100000000)
def flood(surf, y, x, grp):
    """Flood contiguous areas with same group."""
    if surf[y, x] != 0:
        return

    surf[y, x] = grp

    if x > 0:
        flood(surf, y, x - 1, grp)
    if x < (w - 1):
        flood(surf, y, x + 1, grp)
    if y > 0:
        flood(surf, y - 1, x, grp)
    if y < (h - 1):
        flood(surf, y + 1, x, grp)


# fill the area
print("Flooding")

# seed the outside flood
surf[0, 0] = 4

h, w = surf.shape
changes = 1
while changes > 0:
    changes = 0
    for oy in range(h):
        for ox in range(w):
            x = ox
            y = oy
            for diff in range(4):
                if diff == 1 or diff == 3:
                    x = w - x - 1
                if diff == 2 or diff == 3:
                    y = h - y - 1

                if surf[y, x] == 0:

                    if x > 0 and surf[y, x - 1] > 2:
                        surf[y, x] = surf[y, x - 1]
                        changes += 1
                        continue
                    if x < (w - 1) and surf[y, x + 1] > 2:
                        surf[y, x] = surf[y, x + 1]
                        changes += 1
                        continue
                    if y > 0 and surf[y - 1, x] > 2:
                        surf[y, x] = surf[y - 1, x]
                        changes += 1
                        continue
                    if y < (h - 1) and surf[y + 1, x] > 2:
                        surf[y, x] = surf[y + 1, x]
                        changes += 1
                        continue
    # matPrint(surf)
    print("Changes", changes)


# convert 0 to 3
surf[surf == 0] = 3
# convert group 3 to 0
surf[surf == 4] = 0
matPrint(surf)

# now do part 1 again, but checking that the area has no 0
print("Looking for largest areas")
ma = 0
for t1 in tloc:
    for t2 in tloc:
        # skip self
        if t1 == t2:
            continue

        xdiff = t2[0] - t1[0] + 1
        ydiff = t2[1] - t1[1] + 1
        # we only look at rectangles where t1 is to the left of t2
        # reduces duplicate work
        if xdiff < 0:
            continue

        area = xdiff * ydiff
        # print("For", t1, t2, "found area of", area, xdiff, ydiff)

        # is this the largest yet found?
        if area > ma:
            if ydiff > 0:
                # matPrint(surf[t1[1] : t2[1] + 1, t1[0] : t2[0] + 1])
                if np.all(surf[t1[1] : t2[1] + 1, t1[0] : t2[0] + 1] > 0):
                    # print("Increased ma to", area)
                    ma = area
            else:
                # matPrint(surf[t2[1] : t1[1] + 1, t2[0] : t1[0] + 1])
                if np.all(surf[t2[1] : t1[1] + 1, t2[0] : t1[0] + 1] > 0):
                    # print("Increased ma to", area)
                    ma = area

print("#### Part 2 ####")
print("Answer is:", ma)
