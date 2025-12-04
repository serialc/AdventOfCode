"""AoC 2025 Day 04."""

import numpy as np

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


input_file = "input0"
input_file = "input"

raw_surf = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        raw_surf.append(list(line))

surf = np.array(raw_surf)
rlocs = np.where(surf == "@")

accessible = 0
for i in range(len(rlocs[0])):
    x = rlocs[1][i]
    y = rlocs[0][i]

    l = x - 1
    r = x + 1
    t = y - 1
    b = y + 1

    if l < 0:
        l = 0
    if r > surf.shape[1]:
        r = surf.shape[1]
    if t < 0:
        t = 0
    if b > surf.shape[0]:
        b = surf.shape[0]

    # matPrint(surf[t : b + 1, l : r + 1], replace="")
    if np.sum(surf[t : b + 1, l : r + 1] == "@") <= 4:
        accessible += 1

print("#### Part 1 ####")
print("Answer is:", accessible)


# PART 2 ####
print("============ Part 2 start ================")

removed = 0
while True:
    accessible = 0
    rlocs = np.where(surf == "@")
    # matPrint(surf)
    for i in range(len(rlocs[0])):
        x = rlocs[1][i]
        y = rlocs[0][i]

        l = x - 1
        r = x + 1
        t = y - 1
        b = y + 1

        if l < 0:
            l = 0
        if r > surf.shape[1]:
            r = surf.shape[1]
        if t < 0:
            t = 0
        if b > surf.shape[0]:
            b = surf.shape[0]

        # matPrint(surf[t : b + 1, l : r + 1], replace="")
        if np.sum(surf[t : b + 1, l : r + 1] == "@") <= 4:
            accessible += 1
            # remove it
            surf[y, x] = "."
            removed += 1

    # matPrint(surf)
    print(accessible, removed)
    if accessible == 0:
        break

print("#### Part 2 ####")
print("Answer is:", removed)
