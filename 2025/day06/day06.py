"""AoC 2025 Day 06."""

import numpy as np

# from PIL import Image
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

raw = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        raw.append(line.split())
        # print("Line length:", len(line.split()))

# convert to numpy array
math = np.array(raw)

# matPrint(math)

y, x = math.shape

msum = 0
for ix in range(x):
    val = 0
    op = math[y - 1, ix]

    for iy in range(y - 1):
        if op == "+":
            val += int(math[iy, ix])
        if op == "*":
            if val == 0:
                val = int(math[iy, ix])
            else:
                val *= int(math[iy, ix])

    # print(val)
    msum += val


print("#### Part 1 ####")
print("Answer is:", msum)

# PART 2 ####
print("============ Part 2 start ================")

raw = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        raw.append(list(line))

# convert to numpy array
math = np.array(raw)

# matPrint(math)

# split columns by looking for a column full of spaces
coldiv_part = np.where(np.sum(math == " ", axis=0) == math.shape[0])[0]
# add an end delimiter
coldiv = np.append(coldiv_part, math.shape[1])

# total sum
msum = 0
last_col = 0
for cdi in range(len(coldiv)):
    mcol = math[:, last_col : coldiv[cdi]]

    y, x = mcol.shape
    print("Column has following form")
    matPrint(mcol)

    val = 0
    op = mcol[y - 1, 0]
    print("OP is >", op, "<")

    # build vertical number from digits
    for dp in range((x - 1), -1, -1):
        print("Digit pos", dp)
        vertnum_np = mcol[: (y - 1), dp]
        vertnum_str = "".join(vertnum_np)
        vertnum = int(vertnum_str)

        print("We have the number", vertnum)

        if op == "+":
            val += vertnum
        if op == "*":
            if val == 0:
                val = vertnum
            else:
                val *= vertnum

    print("Column solution:", val, "\n")
    msum += val

    # update index of last column
    last_col = coldiv[cdi] + 1

# 16276211366578457 - too high -

print("#### Part 2 ####")
print("Answer is:", msum)
