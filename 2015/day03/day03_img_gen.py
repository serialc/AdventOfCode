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

# make image
pixlist_hw = cmc.makePixelListHw(surf, boost=4, res=3)
cmc.makeRgbImage(pixlist_hw["pixlist"], "day3_part1", pixlist_hw["h"], pixlist_hw["w"])

print("#### Part 1 ####")
print("Answer is:", len(locs))

# PART 2 ####
print("============ Part 2 start ================")

xlim = [0, 0]
ylim = [0, 0]
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
            if sx > xlim[1]:
                xlim[1] = sx
        if d == "<":
            sx -= 1
            if sx < xlim[0]:
                xlim[0] = sx
        if d == "^":
            sy += 1
            if sy > ylim[1]:
                ylim[1] = sy
        if d == "v":
            sy -= 1
            if sy < ylim[0]:
                ylim[0] = sy
        insfor = "bot"
    else:
        if d == ">":
            bx += 1
            if bx > xlim[1]:
                xlim[1] = bx
        if d == "<":
            bx -= 1
            if bx < xlim[0]:
                xlim[0] = bx
        if d == "^":
            by += 1
            if by > ylim[1]:
                ylim[1] = by
        if d == "v":
            by -= 1
            if by < ylim[0]:
                ylim[0] = by
        insfor = "santa"

    sloc = (sx, sy)
    bloc = (bx, by)

    if sloc not in locs:
        locs[sloc] = True
    if bloc not in locs:
        locs[bloc] = True

print(xlim, ylim)
# paint the surface
ssurf = np.zeros((ylim[1] - ylim[0] + 1, xlim[1] - xlim[0] + 1), dtype=np.uint8)
bsurf = np.zeros((ylim[1] - ylim[0] + 1, xlim[1] - xlim[0] + 1), dtype=np.uint8)

# set start based on offset of limits
sx = xlim[0] * -1
sy = ylim[0] * -1
bx = sx
by = sy

surf[y, x] = 1
insfor = "santa"
for d in line:
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

    ssurf[sy, sx] += 1
    bsurf[by, bx] += 1

# scaling
boost = 4
ssurf[ssurf > 0] += boost
bsurf[bsurf > 0] += boost
ssurf = int(255 / ssurf.max()) * ssurf
bsurf = int(255 / bsurf.max()) * bsurf

pixlist = []  # type: ignore
h, w = ssurf.shape
res = 3
for y in range(h):
    for _ in range(res):
        for x in range(w):
            for _ in range(res):
                pixlist.append((ssurf[y, x], bsurf[y, x], 0))

cmc.makeRgbImage(pixlist, "day3_part2", h * res, w * res)

print("#### Part 2 ####")
print("Answer is:", len(locs))
