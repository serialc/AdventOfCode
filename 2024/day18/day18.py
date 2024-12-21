"""AoC 2024 Day 20."""

import numpy as np
import sys

sys.setrecursionlimit(40000)

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

corrupt = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        vals = list([int(z) for z in line.split(",")])
        corrupt.append(vals)

corruption_count = 12
surf_size = 7
corruption_count = 1024
surf_size = 71

surf = np.zeros([surf_size, surf_size], dtype=int)
for c in range(corruption_count):
    x, y = corrupt[c]
    surf[y, x] = 1

matPrint(surf)

# make ca surface
sol_path = surf.copy() * -2
sol_path[sol_path == 0] = -1
# initialize costing
sol_path[0, 0] = 0

next_step = sol_path.copy()

nr, nc = surf.shape

while sol_path[surf_size - 1, surf_size - 1] == -1:
    for y in range(nr):
        for x in range(nc):
            # only do fresh cells
            if next_step[y, x] == -1:
                # look up
                if y > 0 and sol_path[y - 1, x] >= 0:
                    next_step[y, x] = sol_path[y - 1, x] + 1
                # look down
                if y < (nr - 1) and sol_path[y + 1, x] >= 0:
                    next_step[y, x] = sol_path[y + 1, x] + 1
                # look left
                if x > 0 and sol_path[y, x - 1] >= 0:
                    next_step[y, x] = sol_path[y, x - 1] + 1
                # look right
                if x < (nc - 1) and sol_path[y, x + 1] >= 0:
                    next_step[y, x] = sol_path[y, x + 1] + 1

    sol_path = next_step.copy()
    # matPrint(sol_path, cwidth=3, replace=-2, replacement="#")

matPrint(sol_path, cwidth=3, replace=-2, replacement="#")

print("#### Part 1 ####")
print("Answer is:", sol_path[surf_size - 1, surf_size - 1])


# PART 2 ####
print("============ Part 2 start ================")

last_cor = []

# Brute forced it
# - could have jumped around and goldilocked it.

# for c in range(12, len(corrupt)):
for c in range(1024, len(corrupt)):

    last_cor = corrupt[c]
    print("Added corruption", last_cor)

    x, y = corrupt[c]
    # add a new corrupt piece each time
    surf[y, x] = 1

    # make ca surfaces
    sol_path = surf.copy() * -2
    sol_path[sol_path == 0] = -1
    # initialize costing
    sol_path[0, 0] = 0

    while True:
        changes = False

        # create a copy
        next_step = sol_path.copy()

        for y in range(nr):
            for x in range(nc):
                # only do fresh cells
                if next_step[y, x] == -1:
                    # look up
                    if y > 0 and sol_path[y - 1, x] >= 0:
                        changes = True
                        next_step[y, x] = sol_path[y - 1, x] + 1
                    # look down
                    if y < (nr - 1) and sol_path[y + 1, x] >= 0:
                        changes = True
                        next_step[y, x] = sol_path[y + 1, x] + 1
                    # look left
                    if x > 0 and sol_path[y, x - 1] >= 0:
                        changes = True
                        next_step[y, x] = sol_path[y, x - 1] + 1
                    # look right
                    if x < (nc - 1) and sol_path[y, x + 1] >= 0:
                        changes = True
                        next_step[y, x] = sol_path[y, x + 1] + 1

        # point sol_path to next_step
        sol_path = next_step

        # if solved, break to next corruption addition
        if sol_path[surf_size - 1, surf_size - 1] != -1:
            print("Solved with distance of", sol_path[surf_size - 1, surf_size - 1])
            break

        if not changes:
            print("FAILED")
            break

    if not changes:
        break

print("#### Part 2 ####")
print("Answer is:", last_cor)
# 41,26 (x,y) sealed shut path to exit
