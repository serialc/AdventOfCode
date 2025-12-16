"""AoC 2025 Day 08."""

import numpy as np
import math
import time
import sys

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

    if mat.dtype == "float64" or mat.dtype == "int64":
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

nodes = []
with open(input_file, "r") as fh:
    step = 0
    for line in fh:
        line = line.strip("\n")

        nodes.append([int(x) for x in line.split(",")])

print("There are", len(nodes), "nodes in this file")
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
connected = {}  # type: ignore

# make connections
steps = 1000
if input_file == "input0":
    steps = 10
print("Part one will connect", steps, "nodes")

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
consum = {}  # type: ignore
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

# PART 2 ###
print("\n============ Part 2 start ================")

# get the fresh matrix
dmat = dmat2

# Save the shortest connections
connected = {}

# create a string name list of nodes to get the indices easily
snodes = ["_".join([str(x2) for x2 in v]) for v in nodes]

# capture results
mloc = np.zeros(dmat.shape, dtype=int)
dmats = np.zeros(dmat.shape)

stime = time.time()

conn = {}

mi = 0
cnxs = 0
while cnxs < len(nodes) - 1:
    i = mi
    print("Index", i, snodes[i])

    hori = dmat[i, :]
    vert = dmat[:, i]
    shortest = np.min(np.concatenate((dmat[i, :], dmat[:, i])))

    print("Shortest", shortest)
    # if all are infinity, move on to next
    if shortest == np.inf:
        print("Shortest is infinity")
        mi += 1
        cnxs += 1
        quit("All infinity on a line - bad news")

    # print("Node", snodes[i], "wants to pairs with node ", end="")
    if np.any(hori == shortest):
        j = np.where(hori == shortest)[0][0]
        # print(snodes[j], "in column", j)
    elif np.any(vert == shortest):
        j = i
        i = np.where(vert == shortest)[0][0]
        # print(snodes[j], "at row", j)

    # check if nodes are already on same circuit
    if i in conn and j in conn and conn[i] == conn[j]:
        # make that connection infinity
        dmat[i, j] = np.inf
        print("Fail - part of common group", conn[i])
        # and try again
        continue

    # nodes are not on same circuit
    dmats[i, j] = dmat[i, j]
    dmat[i, j] = np.inf
    mloc[i, j] = 1
    print("Connected", i, "to", j)

    # save the nodes to a circuit, join circuits if needed
    if i in conn:
        congroup = conn[i]
    else:
        if len(conn) > 0:
            congroup = conn[max(conn, key=conn.get)] + 1
        else:
            congroup = 1

    # assign a connection group to i
    conn[i] = congroup

    # now we need to either add the same group to the connecting node,
    # or reassign the whole circuit to the same as above

    if j in conn:
        # need to merge all others in group to congroup
        old_congroup = conn[j]
        for key in conn:
            if conn[key] == old_congroup:
                conn[key] = congroup
    else:
        # add node ly to connection group
        conn[j] = congroup

    mi += 1
    cnxs += 1

matPrint(mloc)
matPrint(dmats)
# print(np.max(dmats))
farthest_pair = np.where(dmats == np.max(dmats))
# print(snodes[farthest_pair[0][0]], snodes[farthest_pair[1][0]])
l1 = nodes[farthest_pair[0][0]][0]
l2 = nodes[farthest_pair[1][0]][0]
print(l1, l2)


ftime = time.time() - stime
print("Execution time is", ftime)

# Running time is 979s (16m 19s) and 99% is finding the min and location
# Optimized running time is 622s (10m 22s) and 0% is finding the min and loc
# - Good, moved the burden to the optimizing part but still not adequate
# New strategy - execution time is 0.023210763931274414s
# correct answer for test data, but not my puzzle input!

print("#### Part 2 ####")
print("Answer is:", math.prod((l1, l2)))
