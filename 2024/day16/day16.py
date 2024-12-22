"""AoC 2024 Day 16."""

import numpy as np
import time
import sys
import os.path

sys.setrecursionlimit(40000)

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


def seekEnd(y, x, d, mat, score):
    """Seek the end/E."""
    global lssurf
    global fh

    nr, nc = mat.shape

    # we know the optimal score, can limit processing now
    if score > 109516:
        return 0

    # check we're in bounds and a valid location
    if y == 0 or x == 0 or y == nr - 1 or x == nc - 1 or mat[y, x] == 0:
        return 0

    if lssurf[d][y, x] != -1 and lssurf[d][y, x] < score:
        return 0

    if surf[y, x] == "E":
        print("Found solution", score)
        # fh = open("score_progression.txt", "a")
        # fh.write(str(score) + "\n")
        # fh.close()
        return [score]

    # erase this location - prevent return to it
    mat[y, x] = 0
    # save the directional score
    lssurf[d][y, x] = score

    # continue search, can only turn 90 degrees
    eres, nres, sres, wres = False, False, False, False
    if d == "east":
        eres = seekEnd(y, x + 1, d, mat.copy(), score + 1)
        nres = seekEnd(y - 1, x, "north", mat.copy(), score + 1001)
        sres = seekEnd(y + 1, x, "south", mat.copy(), score + 1001)
    if d == "north":
        nres = seekEnd(y - 1, x, d, mat.copy(), score + 1)
        eres = seekEnd(y, x + 1, "east", mat.copy(), score + 1001)
        wres = seekEnd(y, x - 1, "west", mat.copy(), score + 1001)
    if d == "west":
        wres = seekEnd(y, x - 1, d, mat.copy(), score + 1)
        sres = seekEnd(y + 1, x, "south", mat.copy(), score + 1001)
        nres = seekEnd(y - 1, x, "north", mat.copy(), score + 1001)
    if d == "south":
        sres = seekEnd(y + 1, x, d, mat.copy(), score + 1)
        eres = seekEnd(y, x + 1, "east", mat.copy(), score + 1001)
        wres = seekEnd(y, x - 1, "west", mat.copy(), score + 1001)

    scores = []
    if type(eres) is list:
        scores.extend(eres)
    if type(wres) is list:
        scores.extend(wres)
    if type(nres) is list:
        scores.extend(nres)
    if type(sres) is list:
        scores.extend(sres)

    return scores


input_file = "input0"
input_file = "input1"
input_file = "input"

surf_list = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        surf_list.append(list(line))

surf = np.array(surf_list)

matPrint(surf)

# get start location
start = np.where(surf == "S")
sy, sx = [start[0][0], start[1][0]]

lss = "low_score_surface.npy"

# create a valid path surface
vpsurf = (surf != "#") * 1
vpsurf[vpsurf == 0] = 2

# create or load four lowest score surfaces based on direction
if os.path.exists("n" + lss):
    print("Loading data")
    lssurf = {
        "north": np.load("n" + lss),
        "east": np.load("e" + lss),
        "south": np.load("s" + lss),
        "west": np.load("w" + lss),
    }
else:
    lssurf = {
        "north": (surf != "#") * -1,
        "east": (surf != "#") * -1,
        "south": (surf != "#") * -1,
        "west": (surf != "#") * -1,
    }

stime = time.time()
# main recursive processing start
score = seekEnd(sy, sx, "east", vpsurf.copy(), 0)

if not os.path.exists("n" + lss):
    np.save("n" + lss, lssurf["north"])
    np.save("e" + lss, lssurf["east"])
    np.save("s" + lss, lssurf["south"])
    np.save("w" + lss, lssurf["west"])


print("Processing time", time.time() - stime)

print("#### Part 1 ####")
print("Answer is:", min(score))
# Takes about 8 minutes to find optimal value 109516


# PART 2 ####
print("============ Part 2 start ================")


def seekGoldPath(y, x, d, mat, score):
    """Seek the end/E."""
    nr, nc = mat.shape

    # we know the optimal score, can limit processing now
    if score > 109516:
        return 0

    # check we're in bounds and a valid location
    if y == 0 or x == 0 or y == nr - 1 or x == nc - 1 or mat[y, x] == 0:
        return 0

    # have already found a more efficient path to here
    if lssurf[d][y, x] != -1 and lssurf[d][y, x] < score:
        return 0

    # erase this location - prevent return to it
    mat[y, x] = 0
    # save the directional score
    lssurf[d][y, x] = score

    # found the end
    if surf[y, x] == "E":
        return [mat]

    # continue search, can only turn 90 degrees
    eres, nres, sres, wres = False, False, False, False
    if d == "east":
        eres = seekGoldPath(y, x + 1, d, mat.copy(), score + 1)
        nres = seekGoldPath(y - 1, x, "north", mat.copy(), score + 1001)
        sres = seekGoldPath(y + 1, x, "south", mat.copy(), score + 1001)
    if d == "north":
        nres = seekGoldPath(y - 1, x, d, mat.copy(), score + 1)
        eres = seekGoldPath(y, x + 1, "east", mat.copy(), score + 1001)
        wres = seekGoldPath(y, x - 1, "west", mat.copy(), score + 1001)
    if d == "west":
        wres = seekGoldPath(y, x - 1, d, mat.copy(), score + 1)
        sres = seekGoldPath(y + 1, x, "south", mat.copy(), score + 1001)
        nres = seekGoldPath(y - 1, x, "north", mat.copy(), score + 1001)
    if d == "south":
        sres = seekGoldPath(y + 1, x, d, mat.copy(), score + 1)
        eres = seekGoldPath(y, x + 1, "east", mat.copy(), score + 1001)
        wres = seekGoldPath(y, x - 1, "west", mat.copy(), score + 1001)

    solpaths = []
    if type(eres) is list:
        solpaths.extend(eres)
    if type(wres) is list:
        solpaths.extend(wres)
    if type(nres) is list:
        solpaths.extend(nres)
    if type(sres) is list:
        solpaths.extend(sres)

    return solpaths


sp = seekGoldPath(sy, sx, "east", vpsurf.copy(), 0)
solpaths = np.zeros(vpsurf.shape, dtype=int)
for path in sp:
    solpaths[path == 0] += 1
    # matPrint(path, cwidth=1, replace=2, replacement="#")

matPrint((solpaths > 0) * 1)

print("#### Part 2 ####")
print("Answer is:", np.sum(solpaths > 0))
# 567 - too low: Ugh, forgot to count last cell/E
# 568
