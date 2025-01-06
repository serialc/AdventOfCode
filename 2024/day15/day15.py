"""AoC 2024 Day 15."""

import numpy as np

# import time  # for sleep or measuring duration
# import sys
# import functools  # for memoization
# sys.setrecursionlimit(40000)
# import re


class bcolors:
    """Provide colours for terminal printing."""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def matPrint(mat, cwidth=1, replace=0, replacement=".", hlval=-999):
    """Print a matrix nicely."""
    nh, nw = mat.shape
    print("Dimension", nh, nw)

    for y in range(nh):
        for x in range(nw):
            vlen = len(str(mat[y, x]))
            if mat[y, x] == hlval:
                print(bcolors.OKGREEN, end="")
            if mat[y, x] == replace:
                print(replacement + " " * (cwidth - len(replacement)), end="")
            else:
                print(str(mat[y, x]) + " " * (cwidth - vlen), end="")
            if mat[y, x] == hlval:
                print(bcolors.ENDC, end="")
        print()


def moveBot(mat, d, y, x):
    """Move the robot and any movable boxes."""
    nr, nc = mat.shape

    # don't move if at edge
    if y == 0 or x == 0 or y == (nr - 1) or x == (nc - 1) or mat[y, x] == "#":
        return False

    if d == "^":
        if mat[y - 1, x] != ".":
            if not moveBot(mat, d, y - 1, x):
                return False
        mat[y - 1, x] = mat[y, x]
        mat[y, x] = "."
        return True

    if d == ">":
        if mat[y, x + 1] != ".":
            if not moveBot(mat, d, y, x + 1):
                return False
        mat[y, x + 1] = mat[y, x]
        mat[y, x] = "."
        return True

    if d == "v":
        if mat[y + 1, x] != ".":
            if not moveBot(mat, d, y + 1, x):
                return False
        mat[y + 1, x] = mat[y, x]
        mat[y, x] = "."
        return True

    if d == "<":
        if mat[y, x - 1] != ".":
            if not moveBot(mat, d, y, x - 1):
                return False
        mat[y, x - 1] = mat[y, x]
        mat[y, x] = "."
        return True

    return False


input_file = "input1"
input_file = "input0"
input_file = "input"

surf_list = []
instr_str = ""
with open(input_file, "r") as fh:
    mode = "map"
    for line in fh:
        line = line.strip("\n")

        if line == "":
            mode = "instruct"
            continue

        if mode == "map":
            surf_list.append(list(line))

        if mode == "instruct":
            instr_str += line

# convert data to workable format
surf = np.array(surf_list)
instr = list(instr_str)

# move robot according to instructions
for i in instr:
    bl = np.where(surf == "@")
    y, x = bl[0][0], bl[1][0]
    moveBot(surf, i, y, x)

matPrint(surf, hlval="@")

gps = np.where(surf == "O")
gps_sum = sum(gps[0] * 100) + sum(gps[1])

print("#### Part 1 ####")
print("Answer is:", gps_sum)


# PART 2 ####
print("============ Part 2 start ================")


def pushable(mat, d, y, x):
    """Determines if a block is pushable in a given direction."""
    # Only called for up or down calls
    nr, nc = mat.shape

    # don't move if at edge
    if y == 0 or x == 0 or y == (nr - 1) or x == (nc - 1) or mat[y, x] == "#":
        return False

    if mat[y, x] == ".":
        return True

    # print("Pushing", mat[y, x], "in", d, "from y x", y, x)

    if d == "^":
        incval = -1
    if d == "v":
        incval = 1

    if mat[y, x] == "[":
        # if both blocks above are not clear
        if np.any(mat[y + incval, x : x + 2] != "."):
            # check if each block above is pushable
            return pushable(mat, d, y + incval, x) and pushable(
                mat, d, y + incval, x + 1
            )
        return True

    if mat[y, x] == "]":
        # if both blocks above are not clear
        if np.any(mat[y + incval, x - 1 : x + 1] != "."):
            # check if each block above is pushable
            return pushable(mat, d, y + incval, x - 1) and pushable(
                mat, d, y + incval, x
            )
        return True

    print("pushable was called with direction", d, "which is not valid")
    exit("STOP")


def moveBot2(mat, d, y, x):
    """Move the robot and any movable boxes."""
    nr, nc = mat.shape

    # print("mB2", d, y, x)
    # don't move if at edge
    if y == 0 or x == 0 or y == (nr - 1) or x == (nc - 1) or mat[y, x] == "#":
        return False

    if d == "v":
        incval = 1
    if d == "^":
        incval = -1

    if d in ["^", "v"]:
        # trying to move bot
        if mat[y, x] == "@":
            if mat[y + incval, x] != ".":
                if not moveBot2(mat, d, y + incval, x):
                    return False
            mat[y + incval, x] = mat[y, x]
            mat[y, x] = "."

        # move box
        if mat[y, x] == "[":
            if np.any(mat[y + incval, x : x + 2] != "."):
                # something  in the way, try pushing that
                if pushable(mat, d, y + incval, x) and pushable(
                    mat, d, y + incval, x + 1
                ):
                    moveBot2(mat, d, y + incval, x)
                    moveBot2(mat, d, y + incval, x + 1)
                else:
                    return False

            # actually move the characters
            mat[y + incval, x] = mat[y, x]
            mat[y + incval, x + 1] = mat[y, x + 1]
            mat[y, x] = "."
            mat[y, x + 1] = "."
            return True

        if mat[y, x] == "]":
            if np.any(mat[y + incval, x - 1 : x + 1] != "."):
                # something  in the way, try pushing that
                if pushable(mat, d, y + incval, x - 1) and pushable(
                    mat, d, y + incval, x
                ):
                    moveBot2(mat, d, y + incval, x - 1)
                    moveBot2(mat, d, y + incval, x)
                else:
                    return False

            # actually move the characters
            mat[y + incval, x - 1] = mat[y, x - 1]
            mat[y + incval, x] = mat[y, x]
            mat[y, x - 1] = "."
            mat[y, x] = "."
            return True

    if d == ">":
        if mat[y, x + 1] != ".":
            if not moveBot2(mat, d, y, x + 1):
                return False
        mat[y, x + 1] = mat[y, x]
        mat[y, x] = "."
        return True

    if d == "<":
        if mat[y, x - 1] != ".":
            if not moveBot2(mat, d, y, x - 1):
                return False
        mat[y, x - 1] = mat[y, x]
        mat[y, x] = "."
        return True

    return False


surf_list = []
instr_str = ""

with open(input_file, "r") as fh:
    mode = "map"
    for line in fh:
        line = line.strip("\n")

        if line == "":
            mode = "instruct"
            continue

        if mode == "map":
            # need to spread line
            surf_line = []
            for char in list(line):
                if char == "#":
                    surf_line.append("#")
                    surf_line.append("#")
                if char == "O":
                    surf_line.append("[")
                    surf_line.append("]")
                if char == ".":
                    surf_line.append(".")
                    surf_line.append(".")
                if char == "@":
                    surf_line.append("@")
                    surf_line.append(".")
            surf_list.append(surf_line)

        if mode == "instruct":
            instr_str += line

# convert data to workable format
surf = np.array(surf_list)
instr = list(instr_str)

matPrint(surf, hlval="@")

# move robot according to instructions

move = 1
for i in instr:
    bl = np.where(surf == "@")
    y, x = bl[0][0], bl[1][0]
    moveBot2(surf, i, y, x)

    #  debug
    # print(move, ": Command d y x:", i, y, x)
    # scopy = surf.copy()
    # bl = np.where(scopy == "@")
    # y, x = bl[0][0], bl[1][0]
    # scopy[y, x] = i
    # matPrint(scopy, hlval=i)

    move += 1

matPrint(surf, hlval="@")

# calculate the GPS coordinates
gps = np.where(surf == "[")
gps_sum = sum(gps[0] * 100) + sum(gps[1])

print("#### Part 2 ####")
print("Answer is:", gps_sum)
