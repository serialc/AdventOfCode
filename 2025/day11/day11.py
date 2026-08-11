"""AoC 2025 Day 11."""

import sys
import numpy as np
import functools  # for memoization

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


# memoization
@functools.cache
def pfind(np):
    """Find children of item until 'out' is reached and count branches."""
    if np == "out":
        return 1

    psum = 0
    for p in pdict[np]:
        psum += pfind(p)

    return psum


pdict = dict()

with open(input_file, "r") as fh:
    step = 0
    for line in fh:
        line = line.strip("\n")

        f, t = line.split(": ")
        pdict[f] = t.split(" ")

# print(pdict)

res = -99
if input == "input":
    res = pfind("you")

print("#### Part 1 ####")
print("Answer is:", res)

# PART 2 ###
print("\n============ Part 2 start ================")


# memoization
@functools.cache
def p2find(np, d=0, dac=False, fft=False):
    """Count branches passing 'dac' & 'fft' until 'out' reached."""
    print(" " * d, np, dac, fft)

    if np == "out":
        if dac and fft:
            return 1
        else:
            return 0

    if np == "dac":
        dac = True
    if np == "fft":
        fft = True

    psum = 0
    for p in pdict[np]:

        psum += p2find(p, d + 1, dac, fft)

    return psum


res = p2find("svr")

# 791848918299150 - too high - I had placed the dac/fft detection in the loop
# wrongly giving the following items a positive dac|fft value
print("#### Part 2 ####")
print("Answer is:", res)
