"""AoC 2015 - Day 3."""

import numpy as np
import cmcaoc as cmc

input_file = "input0"
input_file = "input"


with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

# only one line
xlim = [0, 0]
ylim = [0, 0]
x = 0
y = 0
locs = {}
for d in line:
    loc = (x, y)
    if loc not in locs:
        locs[loc] = True

    if d == ">":
        x += 1
        if x > xlim[1]:
            xlim[1] = x
    if d == "<":
        x -= 1
        if x < xlim[0]:
            xlim[0] = x
    if d == "^":
        y += 1
        if y > ylim[1]:
            ylim[1] = y
    if d == "v":
        y -= 1
        if y < ylim[0]:
            ylim[0] = y


# paint the surface
surf = np.zeros((ylim[1] - ylim[0] + 1, xlim[1] - xlim[0] + 1), dtype=np.uint8)

# set start based on offset of limits
x = xlim[0] * -1
y = ylim[0] * -1

surf[y, x] = 1
for d in line:
    if d == ">":
        x += 1
    if d == "<":
        x -= 1
    if d == "^":
        y += 1
    if d == "v":
        y -= 1

    surf[y, x] += 1

cmc.matPrint(surf, cwidth=2)

print("#### Part 1 ####")
print("Answer is:", len(locs))

# PART 2 ####
print("============ Part 2 start ================")

locs = {}
sx, sy = (0, 0)
bx, by = (0, 0)

sloc = (sx, sy)
bloc = (bx, by)

if sloc not in locs:
    locs[sloc] = True
if bloc not in locs:
    locs[bloc] = True

insfor = "santa"
for d in line:

    # alternate instructions
    if insfor == "santa":
        if d == ">":
            sx += 1
        if d == "<":
            sx -= 1
        if d == "^":
            sy += 1
        if d == "v":
            sy -= 1
        insfor = "bot"
    else:
        if d == ">":
            bx += 1
        if d == "<":
            bx -= 1
        if d == "^":
            by += 1
        if d == "v":
            by -= 1
        insfor = "santa"

    sloc = (sx, sy)
    bloc = (bx, by)

    if sloc not in locs:
        locs[sloc] = True
    if bloc not in locs:
        locs[bloc] = True

print("#### Part 2 ####")
print("Answer is:", len(locs))
