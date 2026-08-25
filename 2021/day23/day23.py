"""AoC 2021 - Day 23."""

import cmcaoc as cmc
import numpy as np

# movement energy requirements
mnrg = {"A": 1, "B": 10, "C": 100, "D": 1000}
#
nests = dict()

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
    cmc.matPrint(cave)
    return cave


def roomContents(room, cave):
    """Return contents of room."""
    # get the depth of the cave
    caveh = cave.shape[0] - 1

    if room == "A":
        contents = cave[2:caveh, 3:4].tolist()
    if room == "B":
        contents = cave[2:caveh, 5:6].tolist()
    if room == "C":
        contents = cave[2:caveh, 7:8].tolist()
    if room == "D":
        contents = cave[2:caveh, 9:10].tolist()
    return [x[0] for x in contents]


def roomEmpty(room, cave):
    """Return the status of a room."""
    # get the depth of the cave
    caveh = cave.shape[0] - 1

    return roomContents(room, cave).count("_") == (caveh - 2)


def roomState(room, cave):
    """Return state of room."""
    roomsize = cave.shape[0] - 3

    # Can be 'dirty' or 'fill'
    if roomEmpty(room, cave):
        return "fill"

    # check if present shrimp, if any, are exclusively of the room type
    # and packed to the bottom (not currently doing this, may not be necessary)
    roomcont = roomContents(room, cave)
    if roomcont.count(room) + roomcont.count("_") == roomsize:
        return "fill"

    return "dirty"


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


def distCalc(cave, y, x, surf, dist=0):
    """Calculates distance matrix from location."""

    # print("Loc", y, x, "dist", dist)
    # set location distance
    surf[y, x] = dist

    # check neighbours, not visited and vacant/available
    # up
    if cave[y - 1, x] in ["_", "."] and surf[y - 1, x] == 0:
        distCalc(cave, y - 1, x, surf, dist + 1)
    # down
    if cave[y + 1, x] in ["_", "."] and surf[y + 1, x] == 0:
        distCalc(cave, y + 1, x, surf, dist + 1)
    # left
    if cave[y, x - 1] in ["_", "."] and surf[y, x - 1] == 0:
        distCalc(cave, y, x - 1, surf, dist + 1)
    # right
    if cave[y, x + 1] in ["_", "."] and surf[y, x + 1] == 0:
        distCalc(cave, y, x + 1, surf, dist + 1)

    # does not return as it modifies array passed by reference


def movableSpots(cave, loc):
    """Return the movable locations, distance, outside of the nest."""
    # print("movableSpots - Loc", loc)
    # build matrix of valid spaces - two constraints
    # - are empty '_', and
    valid_dest = (cave == "_") * 1

    # - are on row 1
    valid_dest[2:,] = 0

    # valid destinations above are incomplete (row 1)
    # needs to be dependent on whether nest/home is returnable or not
    # DO THIS
    # DO THIS
    # DO THIS
    # DO THIS
    # DO THIS
    # DO THIS

    # cmc.matPrint(valid_dest)
    # now see which are reachable
    destdist = np.zeros(cave.shape, dtype=int)
    distCalc(cave, *loc, destdist)

    # package the valid destinations and their distance
    valid_destdist = valid_dest * destdist
    vy, vx = np.where(valid_destdist > 0)
    vdest = []
    for i in range(len(vy)):
        y, x = int(vy[i]), int(vx[i])
        vdest.append({"y": y, "x": x, "d": int(valid_destdist[y, x])})

    return vdest


def nestSpot(cave, loc):
    """Return the location and distance to the nest spot."""
    return False


def movableShrimp(cave):
    """Return a list of shrimp that can move."""
    slist = shrimpLocs(cave)

    mshrimp = {}
    for sloc in slist:
        # find whether it can move, and if so, where
        ms = movableSpots(cave, sloc)
        if len(ms) > 0:
            mshrimp[sloc] = ms

    return mshrimp


def route(cave, espent=0):
    """Recursively explore cave movement until solved."""

    # clean_rooms = {"A": False, "B": False, "C": False, "D": False}

    # check if all shrimps are in their nests/home
    # return espent if so
    # DO THIS
    # DO THIS
    # DO THIS
    # DO THIS
    # DO THIS
    # DO THIS

    # get list of shrimp that can move
    ms = movableShrimp(cave)

    # for each shrimp try moving to each location, or not moving (wait)
    for sloc in ms:
        stype = str(cave[sloc])
        print(sloc)

        # moving recursion
        for dest in ms[sloc]:
            print("  ", sloc, dest)
            ncave = np.copy(cave)
            # 'move' the shrimp
            ncave[sloc] = "_"
            ncave[dest["y"], dest["x"]] = stype
            # recursion
            route(ncave, espent + dest["d"] * mnrg[stype])

        # not moving recursion
        route(cave, espent)

    # does shrimp need to leave cave
    # if shloc not in nests[shtype] or
    # print("room empty:", roomEmpty(shtype, cave))
    # print("room state:", roomState(shtype, cave))

    return espent


def tests(data):
    """Run some tests."""
    assert route(data) == 12521
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
    data = loadInput("input0")
    tests(data)

    data = loadInput("input")
    part1(data)

    data = loadInput("input2")
    part2(data)
