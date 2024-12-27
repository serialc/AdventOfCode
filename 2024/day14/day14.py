"""AoC 2024 Day 14."""

import numpy as np
import time  # for sleep or measuring duration

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


def allocRobots(mat, rlist):
    """Place robots on surface."""
    for r in rlist:
        mat[r[0][1], r[0][0]] += 1

    return mat


input_file = "input0"
input_file = "input"

# room is delimited differently for inputs
if input_file == "input":
    sh, sw = [103, 101]
else:
    sh, sw = [7, 11]

surf = np.zeros([sh, sw], dtype=int)

rob = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        p, v = line.split(" ")
        pxy = [int(val) for val in p.split("=")[1].split(",")]
        vxy = [int(val) for val in v.split("=")[1].split(",")]
        rob.append([pxy, vxy])


# matPrint(allocRobots(surf.copy(), rob))

for s in range(100):
    for r in rob:
        # x
        r[0][0] = (r[0][0] + r[1][0]) % sw
        # y
        r[0][1] = (r[0][1] + r[1][1]) % sh

# matPrint(allocRobots(surf.copy(), rob))

# sum quadrants and multiply
robal = allocRobots(surf.copy(), rob)
q1 = np.sum(robal[: int(sh / 2), : int(sw / 2)])
q2 = np.sum(robal[int(sh / 2) + 1 :, : int(sw / 2)])
q3 = np.sum(robal[: int(sh / 2), int(sw / 2) + 1 :])
q4 = np.sum(robal[int(sh / 2) + 1 :, int(sw / 2) + 1 :])
print("Q1 sum", q1)
print("Q2 sum", q2)
print("Q3 sum", q3)
print("Q4 sum", q4)

print("#### Part 1 ####")
print("Answer is:", q1 * q2 * q3 * q4)


# PART 2 ####
print("============ Part 2 start ================")

rob = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        p, v = line.split(" ")
        pxy = [int(val) for val in p.split("=")[1].split(",")]
        vxy = [int(val) for val in v.split("=")[1].split(",")]
        rob.append([pxy, vxy])

for s in range(1, 7848):
    for r in rob:
        # x
        r[0][0] = (r[0][0] + r[1][0]) % sw
        # y
        r[0][1] = (r[0][1] + r[1][1]) % sh

    zcount = max(np.sum(allocRobots(surf.copy() == 1, rob), 0))
    if zcount > 20:
        print("Second", s, "zcount", zcount)
        matPrint(allocRobots(surf.copy(), rob))
        time.sleep(0.01)

print("#### Part 2 ####")
print("Answer is:", "hi2")
# 7747 - too low: bad offset?
# 7748 - too low: aaaah, part1 had already cycled 100
# 7847!
