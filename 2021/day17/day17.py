"""AoC 2021 day17."""

import numpy as np
from PIL import Image
import math

sinput = "target area: x=20..30, y=-10..-5"
sinput = "target area: x=111..161, y=-154..-101"

xra = sinput.split(" ")[2]
xra = xra.split("=")[1].strip(",")
xmin, xmax = xra.split("..")
xmin = int(xmin)
xmax = int(xmax)

yra = sinput.split(" ")[3]
yra = yra.split("=")[1]
ymin, ymax = yra.split("..")
ymin = int(ymin)
ymax = int(ymax)

print(xmin, xmax, ymin, ymax)


def calcPath(xv, yv):
    xp, yp = [0, 0]
    coords = [[xp, yp]]
    maxh = 0

    while xp <= xmax and yp >= ymin:
        # move
        xp += xv
        yp += yv

        if yp > maxh:
            maxh = yp

        coords.append([xp, yp])

        if xp > (xmin - 1) and xp < (xmax + 1) and yp < (ymax + 1) and yp > (ymin - 1):
            return coords, maxh, "good"

        # change velocity
        yv -= 1
        if xv > 0:
            xv -= 1

    if xp > xmax:
        return coords, maxh, "x"
    elif yp < ymin:
        return coords, maxh, "y"
    else:
        return coords, maxh, "xy"


# c,h,r = calcPath(7,2)
# print(r,c,h)
# c,h,r = calcPath(9,0)
# print(r,c,h)
# c,h,r = calcPath(17,-4)
# print(r,c,h)
# c,h,r = calcPath(6,9)
# print(r,c,h)

tx, ty = [1, 1]
tested_velocities = dict()
working_paths = dict()

moh = 0  # max observed height
vymax = 0
for n in range(200):
    c, h, r = calcPath(tx, ty)
    code = str(tx) + "_" + str(ty)

    if r == "y":
        tx += 1
        ty += 1
    if r == "x":
        tx -= 1
    if r == "xy":
        tx -= 1
    if r == "good":
        tested_velocities[code] = True
        working_paths[code] = c
        if h > moh:
            moh = h
            vymax = ty
        ty += 1
    else:
        tested_velocities[code] = False

print("Part 1 - Best height is", moh)

############### Part 2 ##############
print("###### Part 2 ##########")
# Now find what all the initial velocities that could work
# Brute force?

for x in range(xmax + 1):
    for y in range(ymin, vymax + 1):
        code = str(x) + "_" + str(y)
        if code in tested_velocities:
            continue

        c, h, r = calcPath(x, y)
        if r == "good":
            tested_velocities[code] = True
            working_paths[code] = c
        else:
            tested_velocities[code] = False


print("Possible solutions", sum(1 * list(tested_velocities.values())))

############### BONUS ##############
print("###### Bonus  ##########")


def matPrint(mat):
    h, w = mat.shape
    for y in range(h):
        for x in range(w):
            print(mat[y, x], end="")
        print("")


margin = 3
yshift = abs(ymin)
tpad = xmax * 1
xdim = xmax + margin
ydim = tpad + yshift + margin
print("tpad", tpad, "yshift", yshift)

water = np.zeros([ydim, xdim], dtype=int)

for wp, coords in working_paths.items():
    # print(wp, coords)
    for i in range(len(coords) - 1):
        [ix, iy] = coords[i]
        [nx, ny] = coords[i + 1]

        # print("coords", ix,iy, "to", nx,ny)

        xdiff = ix - nx
        ydiff = iy - ny

        if xdiff == 0 and ydiff == 0:
            continue

        # horizontal or vertical
        if ix == nx:
            slope = 999
        else:
            slope = ydiff / xdiff

        # print("slope", slope)
        # if slope > 1, then iterate through y range
        if slope > 1 or slope < -1:
            delta = 1
            if ydiff > 0:
                delta = -1

            # print("More vertical")
            for y in range(iy, ny, delta):
                x = int((y - iy) / (ny - iy) * (nx - ix) + ix)
                if y >= ymin and y < tpad:
                    water[tpad - ydim - y, x] += 1
        if slope <= 1:
            # print("More horizontal")
            for x in range(ix, nx):
                y = int((x - ix) / (nx - ix) * (ny - iy) + iy)
                if y >= ymin and y < tpad:
                    water[tpad - ydim - y, x] += 1

# matPrint(water)

# make graphic
print("Generating image")

magnification = 1
h, w = water.shape
im = Image.new("RGB", (w * magnification, h * magnification))
pixellist = []

maxv = math.log(np.max(water))

for y in range(h):
    for m in range(magnification):
        for x in range(w):
            for m in range(magnification):
                if water[y, x] == 0:
                    pixellist.append((0, 0, 128))
                else:
                    val = math.log(water[y, x]) / maxv
                    pixellist.append((int(128 * val) + 127, int(val), int(val)))

im.putdata(pixellist)  # type: ignore
im.save("probe_paths.png")
