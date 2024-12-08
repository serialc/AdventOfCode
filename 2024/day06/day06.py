"""AoC 2024 - Day 6."""

import numpy as np

# import re


def matPrint(mat, sep=""):
    """
    Print a matrix nicely.

    Takes a numpy 2d array and prints values in a variable
    dense manner.
    """
    nh, nw = mat.shape
    print("Dimension", nh, nw)

    for y in range(nh):
        for x in range(nw):
            print(str(mat[y, x]) + sep, end="")
        print()


input_file = "input0"
input_file = "input"

# get the info

lsurf = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        lsurf.append(list(line))

# convert to np
osurf = np.array(lsurf)


def walkGuard(p2=False, block=(-1, -1)):
    """
    Walk guard along their path.

    Guard walks in straight line unless it hits obstacle.
    It turns right in that case.

    Part 2 determines if an added block at a location forces a infinite cycle.
    """
    # create a copy of the surface
    surf = osurf.copy()

    # get starting location
    g = np.where(surf == "^")
    y = g[0][0]
    x = g[1][0]
    gd = "U"

    # write solution path to sol
    sol = np.zeros(surf.shape, dtype=int)
    # save start location!
    sol[y, x] += 1

    if p2:
        # return False, do not process for a few situations
        if block == (y, x):
            # not allowed to place block at starting location
            return False

        if surf[y, x] == "#":
            return False

        # add the block to the surface
        surf[block] = "#"

    # create a hash/dict to determine past paths and if we're in a loop
    past_paths = {}

    while True:

        # part 2, determine if we're in a loop
        if (gd + str(y) + "_" + str(x)) in past_paths:
            return True
        else:
            past_paths[(gd + str(y) + "_" + str(x))] = True

        # record location only when you arrive
        # in case you 'spin'

        if gd == "U":
            if y == 0:
                break
            if surf[y - 1, x] == "#":
                gd = "R"
            else:
                y -= 1
                sol[y, x] += 1
                continue

        if gd == "D":
            if y == (surf.shape[0] - 1):
                break
            if surf[y + 1, x] == "#":
                gd = "L"
            else:
                y += 1
                sol[y, x] += 1
                continue

        if gd == "R":
            if x == (surf.shape[1] - 1):
                break
            if surf[y, x + 1] == "#":
                gd = "D"
            else:
                x += 1
                sol[y, x] += 1
                continue

        if gd == "L":
            if x == 0:
                break
            if surf[y, x - 1] == "#":
                gd = "U"
            else:
                x -= 1
                sol[y, x] += 1
                continue

    # make easier to read
    field = np.char.chararray(sol.shape, unicode=True)
    field[:] = "."
    field[sol > 0] = "+"
    field[surf == "#"] = "#"

    if not p2:
        matPrint(field)

    if p2:
        return False
    return sol


sol1 = walkGuard()

print("#### Part 1 ####")
print("Answer is:", np.sum(sol1 > 0))
# 4662 too low - forgot to save the start location, off by one!


# PART 2 ####
print("============ Part 2 start ================")

# Just go brute force
# Takes 2 minutes to run

possible_loops = 0
for y in range(osurf.shape[0]):
    # progress report (flush or it won't display)
    print(str(y) + ",", end="", flush=True)

    for x in range(osurf.shape[1]):
        if walkGuard(p2=True, block=(y, x)):
            possible_loops += 1

print("#### Part 2 ####")
print("Answer is:", possible_loops)
