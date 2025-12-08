"""AoC 2025 Day 08."""

import numpy as np
import math
import time

# from PIL import Image
# import sys
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

    if mat.dtype == "float64" or mat.dtype == "int64":
        if value == "":
            value = 0
        nmat = np.full(np.array(mat.shape) + 2 * width, value, dtype=mat.dtype)

    # copy mat contents to new matrix
    nmat[width : mat.shape[0] + width, width : mat.shape[1] + width] = mat

    return nmat


input_file = "input0"
input_file = "input"

nodes = []
with open(input_file, "r") as fh:
    step = 0
    for line in fh:
        line = line.strip("\n")

        nodes.append([int(x) for x in line.split(",")])

# print(nodes)
# create distance matrix
dmat = np.zeros((len(nodes), len(nodes)))

# look at each dimension pair
for xi in range(len(nodes)):
    nx = nodes[xi]
    for yi in range(len(nodes)):
        ny = nodes[yi]

        # only do half the matrix, fill rest with
        if xi <= yi:
            dmat[yi, xi] = np.inf
            continue

        dmat[yi, xi] = math.sqrt(
            math.pow(nx[0] - ny[0], 2)
            + math.pow(nx[1] - ny[1], 2)
            + math.pow(nx[2] - ny[2], 2)
        )

# matPrint(dmat)
dmat2 = dmat.copy()

# Save the shortest connections
connected = {}

# make connections
steps = 10
if input_file == "input":
    steps = 1000

for step in range(steps):

    # get the lowest value from the matrix
    sdist = np.min(dmat)
    ly, lx = [x[0] for x in np.where(dmat == sdist)]

    # print("Connected", nodes[lx], nodes[ly])

    lxs = "_".join([str(v) for v in nodes[lx]])
    lys = "_".join([str(v) for v in nodes[ly]])

    congroup = -1
    if lxs in connected:
        congroup = connected[lxs]
    else:
        # get the next highest group id
        if len(connected) > 0:
            congroup = connected[max(connected, key=connected.get)] + 1
        else:
            congroup = 1

    # add node lx to connection group
    connected[lxs] = congroup

    if lys in connected:
        # need to merge all others in group to congroup
        old_congroup = connected[lys]
        for key in connected:
            if connected[key] == old_congroup:
                connected[key] = congroup

    # add node ly to connection group
    connected[lys] = congroup

    # make the distance large between the two nodes in the matrix
    dmat[ly, lx] = np.inf

    # identify the number of groups

# count occurances of each group
consum = {}
for g in connected.values():
    if g in consum:
        consum[g] += 1
    else:
        consum[g] = 1

consumv = list(consum.values())
consumv.sort(reverse=True)
print("Sorted circuits sizes:", consumv)
# run time 972 seconds

print("#### Part 1 ####")
print("Answer is:", math.prod(consumv[0:3]))
# 777 - Too low - Was sorting ascending, needed to reverse sort

# PART 2 ####
print("============ Part 2 start ================")

# get the fresh matrix
dmat = dmat2

# Save the shortest connections
connected = {}

# create a string name list of nodes to get the indices easily
snodes = ["_".join([str(x2) for x2 in v]) for v in nodes]

# save the lats valid x values
lastvalx = [0, 0]

stime = time.time()
disttime = 0.0

# make connections
while True:

    t0 = time.time()
    # get the lowest value from the matrix
    sdist = np.min(dmat)

    # check if we are done - all nodes connected
    if sdist == np.inf:
        break

    # get the connection ids
    ly, lx = [x[0] for x in np.where(dmat == sdist)]
    t1 = time.time()
    disttime += t1 - t0

    lxs = "_".join([str(v) for v in nodes[lx]])
    lys = "_".join([str(v) for v in nodes[ly]])

    # check if the two nodes are already part of the same circuit group
    if lys in connected and lxs in connected and connected[lys] == connected[lxs]:
        dmat[ly, lx] = np.inf
        continue

    # save the x values in case this is the last node connected
    lastvalx = [nodes[lx][0], nodes[ly][0]]

    congroup = -1
    if lxs in connected:
        congroup = connected[lxs]
    else:
        # get the next highest group id
        if len(connected) > 0:
            congroup = connected[max(connected, key=connected.get)] + 1
        else:
            congroup = 1

    # add node lx to connection group
    connected[lxs] = congroup

    if lys in connected:
        # need to merge all others in group to congroup
        old_congroup = connected[lys]
        for key in connected:
            if connected[key] == old_congroup:
                connected[key] = congroup

    # add node ly to connection group
    connected[lys] = congroup

    # speed optimization
    # for congroup populate matrix distances to infinity between nodes
    if True:
        for xns, g in connected.items():
            if g == congroup:
                for yns, g2 in connected.items():
                    if g2 == congroup:
                        if xns == yns:
                            continue

                        # we have two different nodes that share the same group
                        # put their distance in the matrix to infinity
                        dmat[snodes.index(xns), snodes.index(yns)] = np.inf

    # make the distance large between the two nodes in the matrix
    dmat[ly, lx] = np.inf

ftime = time.time() - stime
print("Execution time is", ftime)
print(
    "Portion of the time finding the minimum and location: ",
    int(disttime / ftime * 100),
    "%",
    sep="",
)

# Running time is 979s (16m 19s) and 99% is finding the min and location
# Optimized running time is 622s (10m 22s) and 0% is finding the min and loc
# - Good, moved the burden to the optimizing part but still not adequate

print("#### Part 2 ####")
print("Answer is:", math.prod(lastvalx))
