"""AoC 2024 Day 20."""

import numpy as np
import sys

# import time
# import re

sys.setrecursionlimit(40000)


def makeFreqDict(items):
    """Get item frequency."""
    fd = dict()
    for item in items:
        if item in fd:
            fd[item] += 1
        else:
            fd[item] = 1
    return fd


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


def solvePath(cy, cx, mat, pmat, dist=0):
    """Follow the path, indicating the distance travelled."""
    sh, sw = mat.shape
    if (
        cy < 0
        or cx < 0
        or cy == sh
        or cx == sw
        or mat[cy, cx] == "#"
        or pmat[cy, cx] != -1
    ):
        return False

    # we are in a new cell/path
    # mark this cell's distance
    pmat[cy, cx] = dist

    if mat[cy, cx] == "E":
        return pmat

    # look for next - only one should work
    if type(solvePath(cy - 1, cx, mat, pmat, dist + 1)) == np.ndarray:
        return pmat
    if type(solvePath(cy + 1, cx, mat, pmat, dist + 1)) == np.ndarray:
        return pmat
    if type(solvePath(cy, cx - 1, mat, pmat, dist + 1)) == np.ndarray:
        return pmat
    if type(solvePath(cy, cx + 1, mat, pmat, dist + 1)) == np.ndarray:
        return pmat


input_file = "input0"
input_file = "input"

surf_list = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        surf_list.append(list(line))

surf = np.array(surf_list)

# get the unique types of plots
# matPrint(surf)

start = np.where(surf == "S")
sty = start[0][0]
stx = start[1][0]
sh, sw = surf.shape

solve_path = solvePath(sty, stx, surf, np.ones(surf.shape, dtype=int) * -1)
solve_dist = np.max(solve_path)

# matPrint(solve_path, cwidth=3, replace=-1, replacement="#")

# Now try cheating in each direction at each step
cheat_paths = []  # type: list[int]
# for each location in path, except the last few
# see if cheating is beneficial
for pd in range(solve_dist):
    pdloc = np.where(solve_path == pd)
    sty = pdloc[0][0]
    stx = pdloc[1][0]

    # is two up shorter? by how much
    if (sty - 2) >= 0 and solve_path[sty - 2, stx] > (pd + 2):
        cheat_paths.append(solve_path[sty - 2, stx] - pd - 2)
    if (sty + 2) < sh and solve_path[sty + 2, stx] > (pd + 2):
        cheat_paths.append(solve_path[sty + 2, stx] - pd - 2)
    if (stx - 2) >= 0 and solve_path[sty, stx - 2] > (pd + 2):
        cheat_paths.append(solve_path[sty, stx - 2] - pd - 2)
    if (stx + 2) < sw and solve_path[sty, stx + 2] > (pd + 2):
        cheat_paths.append(solve_path[sty, stx + 2] - pd - 2)

# print(makeFreqDict(cheat_paths))

print("#### Part 1 ####")
print("Answer is:", sum(np.array(cheat_paths) >= 100))


# PART 2 ####
print("============ Part 2 start ================")


def makeIdentityDiamond(depth):
    """Make a matrix with a diamond of 1's surrounded by 0's."""
    i = np.identity(depth + 1, dtype=bool)
    itop = np.hstack((np.fliplr(i), i[:, 1:]))
    canvas = np.vstack((itop, np.flipud(itop[:depth])))
    for y in range(1, depth * 2):
        breaks = False
        for x in range(1, depth * 2):
            if breaks and canvas[y, x] == 1:
                break
            if canvas[y, x - 1] == 1:
                canvas[y, x] = 1
                breaks = True
    return canvas


def costSurface(y, x, cost, fmat, cmat):
    """Create a cost matrix based on friction/surface cost."""
    mh, mw = fmat.shape

    if y < 0 or x < 0 or y == mh or x == mw or (cmat[y, x] >= 0 and cost >= cmat[y, x]):
        return

    cmat[y, x] = cost

    costSurface(y - 1, x, cost + fmat[y, x], fmat, cmat)
    costSurface(y + 1, x, cost + fmat[y, x], fmat, cmat)
    costSurface(y, x + 1, cost + fmat[y, x], fmat, cmat)
    costSurface(y, x - 1, cost + fmat[y, x], fmat, cmat)


cheat_paths.clear()
# cheat distance
cd = 20
iddi = makeIdentityDiamond(cd)
# pass cost matrix by reference
costsurf = np.ones(iddi.shape, dtype=int) * -1
distmat = costSurface(cd, cd, 0, iddi, costsurf)
# matPrint(costsurf, cwidth=3, replace=-1, replacement="#")
# matPrint(iddi)

# For each point in path, see if there are cheating destinations
# reachable and worthwhile
for pd in range(solve_dist):

    pdloc = np.where(solve_path == pd)
    sty = pdloc[0][0]
    stx = pdloc[1][0]

    # print("=" * 20 + ">", "PD", pd, "YX", sty, stx)

    # get all solve_path values that are
    # greater than sty,stx + manhattan distance to solve_path
    # determine  the limits for literal edge cases
    stymin = sty - cd
    stymax = sty + cd
    stxmin = stx - cd
    stxmax = stx + cd
    i_udist = 0
    i_ddist = cd * 2
    i_ldist = 0
    i_rdist = cd * 2

    if stymin < 0:
        i_udist = cd - sty
        stymin = 0
    if stymax >= sh:
        i_ddist = sh - sty - 1
        stymax = sh - 1
    if stxmin < 0:
        i_ldist = cd - stx
        stxmin = 0
    if stxmax >= sw:
        i_rdist = sw - stx - 1
        stxmax = sw - 1

    # get the AOI - area of interest
    aoi = solve_path[stymin : stymax + 1, stxmin : stxmax + 1]
    # convert to just int and remove values < 0, to zero
    intaoi = aoi.astype(int)
    intaoi[intaoi < 0] = 0
    # trim the identity diamond to match shape
    subiddi = iddi[i_udist : cd + i_ddist + 1, i_ldist : cd + i_rdist + 1]
    # also trim the cost surface
    subcs = costsurf[i_udist : cd + i_ddist + 1, i_ldist : cd + i_rdist + 1]

    # print(intaoi.shape, subiddi.shape)
    # matPrint(intaoi, 3)
    # matPrint(intaoi * subiddi)
    # matPrint(subcs)
    # matPrint(intaoi * subiddi - subcs - pd, cwidth=3)
    # magic happens here:
    # - get the values within identity diamond
    # - that have worthwhile shortcuts compated to distance cost
    worthwhile_shortcuts_matrix = intaoi * subiddi - subcs - pd
    sc = worthwhile_shortcuts_matrix[worthwhile_shortcuts_matrix > 0]
    cheat_paths.extend(sc)
    # print(cheat_paths)


print("#### Part 2 ####")
print("Answer is:", sum(np.array(cheat_paths) >= 100))
