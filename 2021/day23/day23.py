"""AoC 2021 - Day 23."""

import cmcaoc as cmc
import numpy as np

# movement energy requirements
mnrg = {"A": 1, "B": 10, "C": 100, "D": 1000}
nests = dict()  # type: ignore
shnestcol = {"A": 3, "B": 5, "C": 7, "D": 9}

# INFO
# '#' walls
# '.' space to move through at cost
# '_' or letter are places one can rest

# Other rules
# - can't stop at room exits
# - only stop once outside room
# - shrimp only move into their cave if it's either empty or has one of their types there
# - only go to room as final destination (not into someone else's room)
# - each shrimp has two moves max (can move directly from room to own room)


def loadInput(input_file):
    """Retrieve data in usable form."""
    cave = []
    with open(input_file, "r") as fh:
        for line in fh:
            line = line.strip("\n")
            row = []
            colnum = -1

            for c in list(line):
                colnum += 1
                if c == "#":
                    row.append("#")
                    continue
                if c == "*":
                    row.append("_")
                    continue
                if c == ".":
                    row.append(".")
                    continue

                # rest are shrimp
                # spots are occupied
                row.append(c)

            cave.append(row)
    cave = np.array(cave)

    print("Loaded cave system:")
    cmc.matPrint(cave)
    return cave


def shrimpLocs(cave):
    """Return the location of the shrimp."""
    locs = {}
    for shtype in list("ABCD"):

        # careful, np.where returns two arrays of x and y separated
        sy, sx = np.where(cave == shtype)
        stlocs = []
        for i in range(len(sx)):
            stlocs.append([sy[i], sx[i]])

        for stloc in stlocs:
            # clean up from np.int64 to int tuple
            stloc = tuple([int(x) for x in stloc])
            locs[stloc] = shtype
    return locs


def destDistCalc(cave, y, x, surf, dist=0):
    """Calculates distance matrix from location."""
    # does not return as it modifies array passed by reference

    # print("Loc", y, x, "dist", dist)
    # set location distance
    surf[y, x] = dist

    # check neighbours, not visited and vacant/available
    # up
    if cave[y - 1, x] in ["_", "."] and surf[y - 1, x] == 0:
        destDistCalc(cave, y - 1, x, surf, dist + 1)
    # down
    if cave[y + 1, x] in ["_", "."] and surf[y + 1, x] == 0:
        destDistCalc(cave, y + 1, x, surf, dist + 1)
    # left
    if cave[y, x - 1] in ["_", "."] and surf[y, x - 1] == 0:
        destDistCalc(cave, y, x - 1, surf, dist + 1)
    # right
    if cave[y, x + 1] in ["_", "."] and surf[y, x + 1] == 0:
        destDistCalc(cave, y, x + 1, surf, dist + 1)


def movableSpots(cave, loc):
    """Return from loc the possible destinations and distances."""
    # if happily in own nest, return no movable spots
    if isNested(cave, loc):
        return []

    # build matrix of valid/empty spaces
    valid_dest = (cave == "_") * 1

    # which destinations are valid...
    # - foreign nests are never valid
    # - if in foreign nest: own nest and 'outside' are valid
    # - if outside: only own nest is valid

    # foreign nests are never valid
    for sht, ncol in shnestcol.items():
        # preserve own nest destinations, if in 'good standing'
        if cave[loc] == sht and getNestSpot(cave, loc) is not False:
            continue
        valid_dest[2:, ncol] = 0

    # if shrimp is outside, only own nest destinations is valid
    if loc[0] == 1:
        valid_dest[1,] = 0

    # which empty locations are reachable
    destdist = np.zeros(cave.shape, dtype=int)
    destDistCalc(cave, *loc, destdist)

    # package the valid destinations and their distance
    valid_destdist = valid_dest * destdist
    vy, vx = np.where(valid_destdist > 0)

    vdest = []
    for i in range(len(vy)):
        y, x = int(vy[i]), int(vx[i])
        vdest.append({"y": y, "x": x, "d": int(valid_destdist[y, x])})
    return vdest


def getNestContents(cave, shtype):
    """Return the contents of a nest."""
    h, w = cave.shape
    return cave[2 : (h - 1), shnestcol[shtype]]


def isNested(cave, loc):
    """Return whether the shrimp is in a clean nest and no longer needing to move."""
    h, w = cave.shape
    shtype = cave[loc]
    y, x = loc

    # if outside nests, False
    if y == 1:
        return False

    # if in own nest, maybe nesting, if no other shrimp types are present
    is_in_nest_col = x == shnestcol[shtype]
    no_foreign_in_nest = np.all(
        [sp in ["_", shtype] for sp in getNestContents(cave, shtype)]
    )
    if is_in_nest_col and no_foreign_in_nest:
        return True
    # don't worry about shrimp being in correct position
    # - it will always to the deepest part of nest when moving in

    return False


def getNestSpot(cave, loc):
    """Return the location of the deepest nest spot."""
    h, w = cave.shape
    shtype = str(cave[loc])

    # get the contents of this shrimp type's nest
    nest_contents = getNestContents(cave, shtype)

    # find the deepest spot
    deepest = None
    for i in range(len(nest_contents)):
        # if other shrimp is in nest
        if nest_contents[i] not in ["_", shtype]:
            return False
        # see how deep in nest we can get
        if nest_contents[i] == "_":
            deepest = i

    # deepest is False here only if the nest is full
    # we check for nest being full, this shouldn't happen
    if deepest is False:
        cmc.matPrint(cave)
        exit("getNestSpot Error - This should never happen")

    # target nest spot
    ny = deepest + 2
    nx = shnestcol[shtype]
    # print("Deepest", deepest)

    # calculate the distance from loc to nest position
    dcave = np.zeros(cave.shape, dtype=int)
    destDistCalc(cave, *loc, dcave)

    # print(shtype, "nest destination", ny, nx)
    ndist = dcave[ny, nx]
    # check dist, if 0 then it is unreachable from loc
    if ndist == 0:
        return False

    # return dest location with the added the offset and distance from loc
    return {"y": ny, "x": nx, "d": int(ndist)}


def movableShrimp(cave):
    """Return a list of shrimp that can move, their destinations, and distance."""
    slist = shrimpLocs(cave)

    mshrimp = {}
    for sloc in slist:
        # find whether it can move, and if so, where
        ms = movableSpots(cave, sloc)
        if len(ms) > 0:
            mshrimp[sloc] = ms

    return mshrimp


def allShrimpsInTheirNests(cave):
    """Check if all shrimp are in their correct nest."""
    for shtype in list("ABCD"):
        ncon = getNestContents(cave, shtype)
        if not np.all(ncon == shtype):
            return False
    return True


best_score = None
max_depth = None


def route(cave, espent=0, depth=0):
    """Recursively explore cave movement until solved."""
    global best_score
    global max_depth

    # reset best_score
    if depth == 0:
        best_score = None
        max_depth = depth

    if depth > max_depth:
        max_depth = depth

    # check if all shrimps are in their nests/home
    if allShrimpsInTheirNests(cave):
        # print("All Shrimp in nests! E=", espent, "D=", depth, "B=", best_score)
        # cmc.matPrint(cave)
        # print("\n\n")

        # set/update best_score, if valid
        if best_score is None or espent < best_score:
            best_score = espent
            print("All Shrimp in nests! New best E=", espent, "D=", depth)
        return

    # quit if current energy exceeds best score
    if best_score is not None and espent > best_score:
        # print("Return - Current energy (", espent, ") exceeds best score", best_score)
        return

    # print("\nRecursion depth", depth)
    # cmc.matPrint(cave)
    if depth > 32:
        print("Depth", depth)
        print("Shouldn't need more than two moves per shrimp - something's wrong")
        print("Cave situation when limit reached:")
        cmc.matPrint(cave)
        exit("Depth exit")

    # get list of shrimp that can move
    ms = movableShrimp(cave)

    # if nothing can move, no solution in this path
    if len(ms) == 0:
        return

    # for each shrimp:
    # - determine state (happy in nest, out of nest, in bad nest)
    # - try moving to each destination, as needed
    # - let others go first, wait
    for sloc in ms:
        stype = str(cave[sloc])
        y, x = sloc

        # print("Looking at shrimp", stype, "at", sloc)

        # SHRIMP ALREADY IN NEST
        # determine if shrimp is properly nested (not with other types)
        if isNested(cave, sloc):
            # print("Shrimp", stype, "at", sloc, "already nested")
            continue

        # SHRIMP TO NEST
        # if shrimp can properly move to nest, do so
        nspot = getNestSpot(cave, sloc)
        if nspot is not False:
            # move to nest
            # print("Moved shrimp", stype, "to nest at", sloc)
            ncave = np.copy(cave)
            ncave[sloc] = "_"
            ncave[nspot["y"], nspot["x"]] = stype
            # increase energy spent
            # print("--> COST:", mnrg[stype] * nspot["d"])
            route(ncave, espent + mnrg[stype] * nspot["d"], depth + 1)
            # continue
            break

        # shrimp can now only either move out of foreign nest, or wait/do nothing

        # SHRIMP MOVING TO HALLWAY
        # moving recursion
        # the shrimp tries all the possible destinations (outside of nests)
        # print("Moving shrimp possible destinations", ms[sloc])
        for dest in ms[sloc]:
            # if shrimp is outside a foreign nest and can't move to own nest
            # then do nothing
            if y == 1:
                break

            # shrimps are in a foreign nest (and can't move directly to own nest)
            # move to possible locations
            # print("  Moving", stype, "from", sloc, "to", dest)
            ncave = np.copy(cave)
            # 'move' the shrimp
            ncave[sloc] = "_"
            ncave[dest["y"], dest["x"]] = stype

            # recursion
            # print("--> COST:", mnrg[stype] * dest["d"])
            route(ncave, espent + dest["d"] * mnrg[stype], depth + 1)

    if depth == 0:
        print("Solution found!")
        print("Max depth reached was", max_depth)
        print("Best score found is", best_score)
        return best_score


def tests(data):
    """Run some tests."""
    assert route(data) == 12521
    print("All tests passed!")


def tests0(data):
    """Run some tests."""
    assert route(data) == 46
    print("All tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = route(data)
    print("Part 1 answer is:", answer)


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    answer = route(data)
    print("Part 2 answer is:", answer)


if __name__ == "__main__":
    data = loadInput("input1")
    tests0(data)
    data = loadInput("input0")
    tests(data)

    data = loadInput("input")
    part1(data)
    data = loadInput("input2")
    part2(data)
