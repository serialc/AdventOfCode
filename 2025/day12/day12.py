"""AoC 2025 Day 12."""

import sys
import numpy as np
import re
import time

# import functools  # for memoization
# import math
# from PIL import Image


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


shape_dict = {}
spaces = []
with open(input_file, "r") as fh:

    opt = ""
    shape = []
    shapeid = -1
    for line in fh:
        line = line.strip("\n")

        # print("line is", line)

        m = re.findall(r"^(\d+):$", line)
        if m:
            shapeid = int(m[0])
            opt = "shape"
            continue

        sp = re.findall(r"(\d+)x(\d+): (.+)", line)
        if sp:
            w, h, req = sp[0]
            spaces.append([int(w), int(h), [int(x) for x in req.split(" ")]])

        if opt == "shape":
            if line == "":
                # change the shape characters
                shape_dict[shapeid] = (np.array(shape) == "#").astype(np.uint8)
                shape = []
                continue

            shape.append(list(line))
            continue

# print(shape_dict)
# print(spaces)


def giftSqueeze(tasks, surf, depth=0):
    """Make magic."""
    global die

    # print("\ngiftSqueeze!")
    # print(tasks, " " * depth, depth)
    # matPrint(surf)

    if sum(tasks) == 0:
        print("Success!", end="")
        # matPrint(surf)
        return True

    h, w = surf.shape

    # iterate through each shape (next task - nt)
    for nt in np.where(tasks != 0)[0]:

        # retrieve shape to try placing
        tshape = shape_dict[nt]
        sh, sw = tshape.shape

        # print("At depth", depth, "trying to allocate shape id:", nt)
        # matPrint(tshape)
        # try all possible placements

        # get the bounds of existing presents - we only want to add on the edge of these
        if surf.sum() > 0:
            ylim = np.max(np.where(surf.sum(axis=1) > 0)[0]) + 2
            xlim = np.max(np.where(surf.sum(axis=0) > 0)[0]) + 2

            if ylim > (h - sh + 1):
                # print("ylim is shape limited")
                ylim = h - sh + 1
            if xlim > (w - sw + 1):
                # print("xlim is shape limited")
                xlim = w - sw + 1
        else:
            xlim = 1
            ylim = 1

        # print("Depth-bounds", depth, "-", ylim, ",", xlim)

        for tran in range(shape_perms[nt]["t"]):

            if tran > 0:
                # print("Transposed", tran)
                tshape = tshape.T

            for rot in range(shape_perms[nt]["r"]):

                if rot > 0:
                    # print("Rotation", rot)
                    tshape = np.rot90(tshape)

                # Try and allocate this shape in all locations
                # matPrint(tshape)

                for y in range(ylim):
                    for x in range(xlim):
                        if die:
                            return False

                        # fit it in each configuration
                        if np.all(surf[y : y + sh, x : x + sw] + tshape < 2):

                            csurf = surf.copy()
                            ctasks = tasks.copy()
                            # update surface
                            csurf[y : y + sh, x : x + sw] = (
                                csurf[y : y + sh, x : x + sw] + tshape
                            )
                            # update tasks
                            ctasks[nt] -= 1
                            if giftSqueeze(ctasks, csurf, depth + 1):
                                return True
    # didn't succeed
    die = True
    return False


# LOOK AT THE AREA versus INPUT AREAS --- obvious?
proportions = []
for sp in spaces:
    space = np.zeros((sp[1], sp[0]), dtype=np.uint8)
    tasks = np.array(sp[2])
    gift_areas = [np.sum(shape_dict[i]) * tasks[i] for i in range(len(tasks))]
    fill = np.sum(gift_areas) / np.prod(space.shape)

    proportions.append(round(fill, 3))
# print(proportions)
print("Quick answer is:", sum(np.array(proportions) < 1))

if input_file == "input":
    # create new shapes that are compact combinations of given shapes
    shape_dict[6] = np.zeros((4, 4), dtype=np.uint8)
    shape_dict[6][0:3, 0:3] += shape_dict[0]
    shape_dict[6][1:4, 0:3] += np.rot90(shape_dict[0], 2)

    shape_dict[7] = np.zeros((4, 4), dtype=np.uint8)
    shape_dict[7][0:3, 0:3] += np.rot90(shape_dict[3], 2)
    shape_dict[7][1:4, 1:4] += shape_dict[3]

    shape_dict[8] = np.zeros((4, 4), dtype=np.uint8)
    shape_dict[8][0:3, 0:3] += shape_dict[4]
    shape_dict[8][1:4, 0:3] += np.rot90(shape_dict[4], 2)

    shape_dict[9] = np.zeros((5, 5), dtype=np.uint8)
    shape_dict[9][0:3, 0:3] += np.rot90(shape_dict[5], 2)
    shape_dict[9][2:5, 0:3] += shape_dict[5]

# for each tree area replace individual occurances with the joined
for spi in range(len(spaces)):
    # replace '0' occurances with half the number of '6'
    spaces[spi][2].append(int(spaces[spi][2][0] / 2))
    spaces[spi][2][0] %= 2

    # replace '3' occurances with half the number of '7'
    spaces[spi][2].append(int(spaces[spi][2][3] / 2))
    spaces[spi][2][3] %= 2

    # replace '4' occurances with half the number of '8'
    spaces[spi][2].append(int(spaces[spi][2][4] / 2))
    spaces[spi][2][4] %= 2

    # replace '5' occurances with half the number of '9'
    spaces[spi][2].append(int(spaces[spi][2][5] / 2))
    spaces[spi][2][5] %= 2

# characterize each shape
shape_perms = []
for shid in shape_dict:
    sh = shape_dict[shid]
    perms = {"t": 2, "r": 4}

    # shape needs only be rotated once
    if (sh == np.fliplr(sh)).all() and (sh == np.flipud(sh)).all():
        perms["t"] = 1
        perms["r"] = 2

    # shape doesn't need to be flipped, only rotated
    if (
        (sh == sh.T).all()
        or (np.rot90(sh.T, 2) == sh).all()
        or (sh == np.fliplr(sh)).all()
        or (sh == np.flipud(sh)).all()
    ):
        perms["t"] = 1

    shape_perms.append(perms)

    # print("\nShape", shid)
    # matPrint(sh)

# now allocate required shapes in spaces
total_gifts = 0
for sp in spaces:
    die = False
    print("Task", sp, end=" ")
    space = np.zeros((sp[1], sp[0]), dtype=np.uint8)
    tasks = np.array(sp[2])

    stime = time.time()
    if giftSqueeze(tasks, space):
        total_gifts += 1
    else:
        print("Failed!", end="")
    print("", time.time() - stime)

print("#### Part 1 ####")
print("Answer is:", total_gifts)
