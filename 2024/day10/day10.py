"""AoC 2024 Day 10."""

import numpy as np

# import re


def matPrint(mat, sep=""):
    """Print a matrix nicely."""
    nh, nw = mat.shape
    print("Dimension", nh, nw)

    for y in range(nh):
        for x in range(nw):
            print(str(mat[y, x]) + sep, end="")
        print()


def trailHeadSearch(y, x, last_val, mat, start=False):
    """Recursively searches for a peak (9 value)."""
    # is it out of bounds?
    if y < 0 or x < 0 or y == surf.shape[0] or x == surf.shape[1]:
        return None

    # print(y, x, last_val, surf[y, x])

    # is this a valid (+1) raise from last elev?
    if surf[y, x] != (last_val + 1) and not start:
        return None

    # trace path
    mat[y, x] = surf[y, x]

    # is this a peak/9?
    if surf[y, x] == 9:
        # matPrint(mat)
        return [str(y) + "_" + str(x)]

    th_count = []
    up = trailHeadSearch(y + 1, x, surf[y, x], mat)
    if up is not None:
        th_count.extend(up)
    down = trailHeadSearch(y - 1, x, surf[y, x], mat)
    if down is not None:
        th_count.extend(down)
    left = trailHeadSearch(y, x - 1, surf[y, x], mat)
    if left is not None:
        th_count.extend(left)
    right = trailHeadSearch(y, x + 1, surf[y, x], mat)
    if right is not None:
        th_count.extend(right)

    return th_count


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

surf = np.array(surf_list, dtype=int)

# get trail heads
trail_heads = np.where(surf == 0)
th_vals = []
for i in range(len(trail_heads[0])):
    # print("Trail head", trail_heads[0][i], trail_heads[1][i])
    th_surf = np.zeros(surf.shape, dtype=int)
    th_paths = trailHeadSearch(
        trail_heads[0][i], trail_heads[1][i], 0, th_surf, start=True
    )
    # matPrint(th_surf)

    # there are multiple roots to a peak - remove duplicates
    th_count = len(np.unique(np.array(th_paths)))
    th_vals.append(th_count)

# print(th_vals)

print("#### Part 1 ####")
print("Answer is:", sum(th_vals))


# PART 2 ####
print("============ Part 2 start ================")

th_vals = []
for i in range(len(trail_heads[0])):
    # print("Trail head", trail_heads[0][i], trail_heads[1][i])
    th_surf = np.zeros(surf.shape, dtype=int)
    th_paths = trailHeadSearch(
        trail_heads[0][i], trail_heads[1][i], 0, th_surf, start=True
    )
    # matPrint(th_surf)

    # there are multiple roots to a peak
    # this is now fine
    th_count = len(th_paths)
    th_vals.append(th_count)

print("#### Part 2 ####")
print("Answer is:", sum(th_vals))
