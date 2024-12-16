"""AoC 2024 Day 12."""

import numpy as np
import sys
import time

# import re


def matPrint(mat, sep=""):
    """Print a matrix nicely."""
    nh, nw = mat.shape
    print("Dimension", nh, nw)

    for y in range(nh):
        for x in range(nw):
            print(str(mat[y, x]) + sep, end="")
        print()


def regionBloom(y, x, grp, smat, dmat, diagonal=False):
    """Expand grp recursively."""
    # dmat is initialized as -1
    if dmat[y, x] != 0:
        return

    dmat[y, x] = grp

    mh, mw = smat.shape
    # up
    if y > 0 and smat[y - 1, x]:
        regionBloom(y - 1, x, grp, smat, dmat, diagonal)
    # down
    if y < (mh - 1) and smat[y + 1, x]:
        regionBloom(y + 1, x, grp, smat, dmat, diagonal)
    # left
    if x > 0 and smat[y, x - 1]:
        regionBloom(y, x - 1, grp, smat, dmat, diagonal)
    # right
    if x < (mw - 1) and smat[y, x + 1]:
        regionBloom(y, x + 1, grp, smat, dmat, diagonal)

    if diagonal:
        # up-right
        if y > 0 and x < (mw - 1) and smat[y - 1, x + 1]:
            regionBloom(y - 1, x + 1, grp, smat, dmat, diagonal)
        # down-right
        if y < (mh - 1) and x < (mw - 1) and smat[y + 1, x + 1]:
            regionBloom(y + 1, x + 1, grp, smat, dmat, diagonal)
        # left-down
        if x > 0 and y < (mh - 1) and smat[y + 1, x - 1]:
            regionBloom(y + 1, x - 1, grp, smat, dmat, diagonal)
        # up-left
        if x < 0 and y > 0 and smat[y - 1, x + 1]:
            regionBloom(y - 1, x + 1, grp, smat, dmat, diagonal)

    # as we write to reference, no need to return anything
    return


def fenceFlood(y, x, mat, history={}):
    """Flood the space and count the boundaries with other crop types, the fences."""
    if y < 0 or x < 0 or y == mat.shape[0] or x == mat.shape[1] or mat[y, x] == 0:
        return 0

    # don't visit a crop cell we've already visited
    loc_code = str(y) + "_" + str(x)
    if loc_code in history:
        return 0

    history[loc_code] = True

    # print("Processing", loc_code)
    seg_count = 0
    # look up, down, left, right
    if y == 0 or (y > 0 and mat[y - 1, x] == 0):
        seg_count += 1
    if (y == mat.shape[0] - 1) or (y < mat.shape[0] - 1 and mat[y + 1, x] == 0):
        seg_count += 1
    if x == 0 or (x > 0 and mat[y, x - 1] == 0):
        seg_count += 1
    if (x == mat.shape[1] - 1) or (x < mat.shape[1] - 1 and mat[y, x + 1] == 0):
        seg_count += 1
    # print(loc_code, "Local fence", seg_count)

    seg_count += fenceFlood(y - 1, x, mat, history)
    seg_count += fenceFlood(y + 1, x, mat, history)
    seg_count += fenceFlood(y, x - 1, mat, history)
    seg_count += fenceFlood(y, x + 1, mat, history)

    # print(loc_code, "Total fence", seg_count)
    return seg_count


def cropGrouping(csurf, diag=False):
    """Determine which region each crop belongs to."""
    mh, mw = csurf.shape

    region_id = 1
    regions = np.zeros(csurf.shape, dtype=int)
    for y in range(mh):
        for x in range(mw):
            # if this is a crop of our selected type (csurf[y,x] == True)
            # and we haven't classified which region it belongs to (regions[y,x] == 0)
            if csurf[y, x] and regions[y, x] == 0:
                regionBloom(y, x, region_id, csurf, regions, diagonal=diag)
                region_id += 1
    return regions


def fenceWalk(y, x, direction, seg_count, mat, history={}, debug=False):
    """
    Walk the perimeter of a region and count the segments.

    Location y, x is always within the region.
    Segments are the 'sides' of a region.
    Code follows the 'left' side while walking forward.
    Algorithm doesn't deal with inner holes
    """
    loc_code = str(y) + "_" + str(x) + "_" + direction
    if loc_code in history:
        return seg_count

    history[loc_code] = direction
    if debug:
        print("Direction", direction)

    if direction == "right":
        # turn down - at top (can't go up) or no region above AND
        # - we are at the right 'wall'
        # - no region to the right
        if (y == 0 or mat[y - 1, x] == 0) and (
            x == (mat.shape[1] - 1) or mat[y, x + 1] == 0
        ):
            return fenceWalk(y, x, "down", seg_count + 1, mat, history, debug)
        # turn up - above is part of region
        if y > 0 and mat[y - 1, x] == 1:
            return fenceWalk(y - 1, x, "up", seg_count + 1, mat, history, debug)
        # continue right
        return fenceWalk(y, x + 1, direction, seg_count, mat, history, debug)

    if direction == "down":
        # turn left - at right or no region to right AND
        # - we are at the bottom 'wall'
        # - and no region below
        if (x == (mat.shape[1] - 1) or mat[y, x + 1] == 0) and (
            y == (mat.shape[0] - 1) or mat[y + 1, x] == 0
        ):
            return fenceWalk(y, x, "left", seg_count + 1, mat, history, debug)
        # turn right - to the right is part of region
        if x < (mat.shape[1] - 1) and mat[y, x + 1] == 1:
            return fenceWalk(y, x + 1, "right", seg_count + 1, mat, history, debug)
        # continue down
        return fenceWalk(y + 1, x, direction, seg_count, mat, history, debug)

    if direction == "up":
        # turn right - at left wall or no region to the left AND
        # - we are at the top 'wall' OR
        # - no region above
        if (x == 0 or mat[y, x - 1] == 0) and (y == 0 or mat[y - 1, x] == 0):
            return fenceWalk(y, x, "right", seg_count + 1, mat, history, debug)
        # turn left - to the left is part of the region
        if x > 0 and mat[y, x - 1] == 1:
            return fenceWalk(y, x - 1, "left", seg_count + 1, mat, history, debug)
        # keep moving up
        return fenceWalk(y - 1, x, direction, seg_count, mat, history, debug)

    if direction == "left":
        # turn up - at bottom or no region below AND
        # - we are at the left 'wall' OR
        # - no region left
        if (y == (mat.shape[0] - 1) or mat[y + 1, x] == 0) and (
            x == 0 or mat[y, x - 1] == 0
        ):
            return fenceWalk(y, x, "up", seg_count + 1, mat, history, debug)
        # turn down - down is part of the region
        if y < (mat.shape[0] - 1) and mat[y + 1, x] == 1:
            return fenceWalk(y + 1, x, "down", seg_count + 1, mat, history, debug)
        # keep moving left
        return fenceWalk(y, x - 1, direction, seg_count, mat, history, debug)


def escapeInterior(y, x, mat, history):
    """
    Look for diagonal connection outside of region.

    Matrix should look like this:

    00000000
    00111100
    00122100
    00011100 <- True
    00000000
      ^
      True
    """
    # if out of bounds or target is not a '2'
    if x < 0 or y == mat.shape[0] or x == mat.shape[1] or mat[y, x] != 2:
        return False

    # don't visit a crop cell we've already visited
    loc_code = str(y) + "_" + str(x)
    if loc_code in history:
        return False

    # track visits
    history[loc_code] = True

    if (
        mat[y + 1, x + 1] == 0
        or mat[y - 1, x - 1] == 0
        or mat[y + 1, x - 1] == 0
        or mat[y - 1, x + 1] == 0
    ):
        return True

    # Try the von neumann neighbours
    return (
        escapeInterior(y + 1, x, mat, history)
        or escapeInterior(y - 1, x, mat, history)
        or escapeInterior(y, x + 1, mat, history)
        or escapeInterior(y, x - 1, mat, history)
    )


def deFence(mat):
    """
    Count the number of fence segments around a crop region.

    check each plant's Von Neuman neighbours
    if the same region, remove the fence
    now reduce the perimeter
    fenceFlood() is about 10x faster - this is no longer used
    """
    plants_count = np.sum(mat > 0)

    # Imagine a fence around each individual plant
    # set perimeter max
    plant_perimeter = plants_count * 4

    [mh, mw] = mat.shape
    for y in range(mh):
        for x in range(mw):
            if mat[y, x] == 1:
                # then look in each direction

                # up
                if y > 0 and mat[y - 1, x] == 1:
                    plant_perimeter -= 1
                # down
                if y < (mh - 1) and mat[y + 1, x] == 1:
                    plant_perimeter -= 1
                # left
                if x > 0 and mat[y, x - 1] == 1:
                    plant_perimeter -= 1
                # right
                if x < (mw - 1) and mat[y, x + 1] == 1:
                    plant_perimeter -= 1

    return plant_perimeter


def countCorners(mat):
    """Count the corners of a contiguous area."""

    # add buffer around matrix -> bm
    bm = np.zeros(np.array(mat.shape) + 2, dtype=int)
    bm[1:-1, 1:-1] = mat

    [bmh, bmw] = bm.shape

    idm = np.identity(2, dtype=bool)
    # 1 0
    # 0 1
    fidm = np.fliplr(idm)
    # 0 1
    # 1 0

    corner_count = 0
    for y in range(bmh):
        for x in range(bmw):
            if bm[y, x] == 1:
                # tl corner
                if np.all(bm[y - 1 : y + 1, x - 1 : x + 1][fidm] == 0):
                    corner_count += 1
                # tr corner
                if np.all(bm[y - 1 : y + 1, x : x + 2][idm] == 0):
                    corner_count += 1
                # bl corner
                if np.all(bm[y : y + 2, x - 1 : x + 1][idm] == 0):
                    corner_count += 1
                # br corner
                if np.all(bm[y : y + 2, x : x + 2][fidm] == 0):
                    corner_count += 1

                # Do it again for inner corners
                # tl inner corner
                if bm[y + 1, x + 1] == 0 and np.all(
                    bm[y : y + 2, x : x + 2][fidm] == 1
                ):
                    corner_count += 1
                # tr corner
                if bm[y + 1, x - 1] == 0 and np.all(
                    bm[y : y + 2, x - 1 : x + 1][idm] == 1
                ):
                    corner_count += 1
                # bl corner
                if bm[y - 1, x + 1] == 0 and np.all(
                    bm[y - 1 : y + 1, x : x + 2][idm] == 1
                ):
                    corner_count += 1
                # br corner
                if bm[y - 1, x - 1] == 0 and np.all(
                    bm[y - 1 : y + 1, x - 1 : x + 1][fidm] == 1
                ):
                    corner_count += 1

    return corner_count


input_file = "input0"
input_file = "input1"
input_file = "input2"
input_file = "input3"
input_file = "input4"
input_file = "input5"
input_file = "input"

surf_list = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        surf_list.append(list(line))

surf = np.array(surf_list)

# get the unique types of plots
# matPrint(surf)

crop_types = np.unique(surf)
sh, sw = surf.shape

crop_data = {}  # type: dict[str, int]
fence_cost = 0
for crop in crop_types:

    # for this crop determine which region each crop belongs to
    regions = cropGrouping(surf == crop)

    # matPrint(regions)
    region_ids = list(np.unique(regions))
    region_ids.remove(0)

    # for each region of the crop
    for region in region_ids:
        # create our crop region surface
        rsurf = (regions == region) * 1

        # matPrint(rsurf)
        plants_count = np.sum(rsurf > 0)

        rlocs = np.where(rsurf == 1)
        y = rlocs[0][0]
        x = rlocs[1][0]
        plant_perimeter = fenceFlood(y, x, rsurf)

        # crop region code
        crc = crop + str(region)
        # print(crc, plants_count, plant_perimeter)
        crop_data[crc] = plants_count * plant_perimeter
        fence_cost += crop_data[crc]


print("#### Part 1 ####")
print("Answer is:", fence_cost)


# PART 2 ####
print("============ Part 2 start ================")

# reset data and costs
crop_data.clear()
fence_cost = 0

sys.setrecursionlimit(40000)
internals_count = 0
matPrint(surf)

corner_sum = time.time() - time.time()
walking_sum = time.time() - time.time()

for crop in crop_types:
    print(crop)

    # for this crop determine which region each crop belongs to
    regions = cropGrouping(surf == crop)

    print("Regions of ", crop)
    # matPrint(regions)
    region_ids = list(np.unique(regions))
    region_ids.remove(0)

    # for each region of the crop
    for region in region_ids:
        # crop region code
        crc = crop + str(region)

        # create our crop region surface
        rsurf = (regions == region) * 1

        # matPrint(rsurf)
        # sum plants in crop region
        plants_count = np.sum(rsurf > 0)

        # find the highest, and then leftmost corner of the region
        rlocs = np.where(rsurf == 1)
        y = rlocs[0][0]
        x = rlocs[1][0]

        c_time = time.time()
        corner_count = 4
        if plants_count > 2:
            corner_count = countCorners(rsurf)
        corner_sum += time.time() - c_time

        # count the sides of the region
        w_time = time.time()
        sides_count = fenceWalk(y, x, "right", 0, rsurf, debug=False)

        # create a buffer region around the surface remove
        # areas trapped against the edge that could appear
        # as interior by our algorithm
        brsurf = np.zeros(np.array(rsurf.shape) + 2, dtype=int)
        brsurf[1:-1, 1:-1] = rsurf

        # now need to substrack any interior fences
        # let's get the number of groups to see if there's some interiors
        icg_surf = cropGrouping(brsurf == 0, diag=True)
        # print("Groupings other than the target crop")
        # matPrint(icg_surf)

        icg_vals = list(np.unique(icg_surf))
        # remove 0, that's the target region, are not interested
        icg_vals.remove(0)

        # ICG != 1 are candidate internal areas
        # however need to check a few things

        # if there's an interior, calculate it's perimeter
        # what contitues an interior is tricky
        # they can't be on the edge or diagonally connected to outside
        if len(icg_vals) > 1:

            # print("There may be an interior")
            # iterate through thte candidate interior areas
            # ignore 1 as this is considered the outside
            for inner_target in range(2, len(icg_vals) + 1):

                # extract the inner group
                it_surf = (icg_surf == inner_target) * 1

                # get the top/left corner of the crop region to
                # calculate the fence sides
                ilocs = np.where(it_surf == 1)
                iy = ilocs[0][0]
                ix = ilocs[1][0]

                # matPrint(it_surf * 2 + brsurf)

                # Now, careful, we want to walk the main crop - not the inner crop!
                # To do this we shift the fenceWalk:
                # - surface
                # - start location, and
                # - direction
                inner_sides_count = fenceWalk(
                    iy, ix - 1, "down", 0, brsurf, debug=False
                )
                # print("ISC", inner_sides_count)
                sides_count += inner_sides_count
                internals_count += 1
        walking_sum += time.time() - w_time

        # if sides_count != corner_count:
        # matPrint(rsurf)
        # print("Counts: walking", sides_count, "cornering", corner_count)
        # exit("BAD MATCH")

        # Summarize the crop region
        print(crc, plants_count, sides_count, corner_count)
        # crop_data[crc] = plants_count * sides_count
        crop_data[crc] = plants_count * corner_count
        fence_cost += crop_data[crc]

print("Corner count", corner_sum)
print("Walking count", walking_sum)

print("Internals count", internals_count)

print("#### Part 2 ####")
print("Answer is:", fence_cost)
# 833540 too low - not ignoring inner areas
# 688684 too low - silly me, don't subtract, add them! Need to go up!
# 978396 too high - Wasn't doing it right, bug.
# 871116 no info - 'Interior' region on edge are not interior! Double counted!
# 869044 no info - Diagonally connected inner areas are not considered inner by
#     fenceWalk! Need to remove 'inner' values that have any diagonal connection
#     outside of region surface
# 857500 no info - Wow this is crushing. This is what Aurélien meant about mental health
#     Inner regions diagonally touching another inner region considered wrongly external
# 869044 no info - X_X
#     Didn't fix the problem really, because diagonal regions can chain... See input4
# 860104 no info - Q_Q
#     I was 'walking' the inner crop rather than the interior edge of the target crop
# 881390 no info - (✖╭╮✖)
# 858684 - created corner counting, rather than side, works!
#     fenceWalk isn't working correctly, wasn't able to resolve problems with input5
#     - too bad because it may be more efficient
