"""AoC 2025 Day 04."""

import numpy as np
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

raw_surf = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        raw_surf.append(list(line))

# convert to numpy array
surf = np.array(raw_surf)
# add border to make neighbourhood work on the edges more easily
surf = matWrap(surf, value="#")
# find the locations of all the rolls of paper
rlocs = np.where(surf == "@")

accessible = 0
for i in range(len(rlocs[0])):
    x = rlocs[1][i]
    y = rlocs[0][i]

    if np.sum(surf[(y - 1) : (y + 2), (x - 1) : (x + 2)] == "@") <= 4:
        accessible += 1

print("#### Part 1 ####")
print("Answer is:", accessible)


# PART 2 ####
print("============ Part 2 start ================")

# img size multiplier
resmult = 2
pid = 1

removed = 0
palhex = [
    "d53e4f",
    "f46d43",
    "fdae61",
    "fee08b",
    "ffffbf",
    "e6f598",
    "abdda4",
    "66c2a5",
    "3288bd",
]
paldec = []  # type: ignore
for ph in palhex:
    paldec.append((int(ph[:2], 16), int(ph[2:4], 16), int(ph[4:], 16)))

while True:
    im = Image.new("RGB", (surf.shape[0] * resmult, surf.shape[1] * resmult))
    # make image frame
    pixellist = []
    for y in range(surf.shape[0]):
        for mult in range(resmult):
            for x in range(surf.shape[1]):
                for mult in range(resmult):
                    if surf[y, x] == "#":
                        pixellist.append((0, 0, 0))
                    if surf[y, x] == ".":
                        pixellist.append((10, 10, 10))
                    if surf[y, x] == "@":
                        ncount = np.sum(
                            surf[(y - 1) : (y + 2), (x - 1) : (x + 2)] == "@"
                        )
                        pixellist.append(paldec[ncount - 1])
                        # pixellist.append((255, 255, 255))
    im.putdata(pixellist)  # type: ignore
    im.save("img_" + "0" * (3 - len(str(pid))) + str(pid) + ".png")
    pid += 1

    accessible = 0
    rlocs = np.where(surf == "@")
    # matPrint(surf)
    for i in range(len(rlocs[0])):
        x = rlocs[1][i]
        y = rlocs[0][i]

        # matPrint(surf[t : b + 1, l : r + 1], replace="")
        if np.sum(surf[(y - 1) : (y + 2), (x - 1) : (x + 2)] == "@") <= 4:
            accessible += 1
            # remove it
            surf[y, x] = "."
            removed += 1

    # matPrint(surf)
    print(accessible, removed)
    if accessible == 0:
        break

matPrint(surf)
print("#### Part 2 ####")
print("Answer is:", removed)
