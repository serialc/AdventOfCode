"""AoC 2015 - Day 6."""

import re


def doSplit(sl, s, hvd, val):
    """Split out two areas."""
    # print("->", hvd, "split", s, "at", val)

    if hvd == "h":
        sl.append([s[0], s[1], val - 1, s[3], s[4], s[5], s[6]])
        sl.append([s[0], val, s[2], s[3], s[4], s[5], s[6]])

    if hvd == "v":
        sl.append([s[0], s[1], s[2], s[3], val - 1, s[5], s[6]])
        sl.append([s[0], s[1], s[2], val, s[4], s[5], s[6]])

    if hvd == "d":
        sl.append([s[0], s[1], s[2], s[3], s[4], s[5], val - 1])
        sl.append([s[0], s[1], s[2], s[3], s[4], val, s[6]])


def cubesSplit(sl, b, t, l, r, f, d):
    """Divides light list into smaller lists."""
    # print("#cubesSplit()", b, t, l, r, f, d)
    while True:
        # track if we've done splits, delete former bounds
        delind = []

        # iterate through state list (sl)
        for i in range(len(sl)):
            s = sl[i]
            sbot, stop, sleft, sright, sfront, sback = s[1:]

            # for efficiency - check left/right and front/back are in bounds
            if sleft <= r and sright >= l and sfront <= d and sback >= f:
                # do the 'horizontal' splits
                if sbot < b and b <= stop:
                    # print("Bottom split")
                    doSplit(sl, s, "h", b)
                    delind.append(i)
                    break
                if sbot <= t and t < stop:
                    # print("Top split")
                    doSplit(sl, s, "h", t + 1)
                    delind.append(i)
                    break

            # for efficiency - check bottom/top and front/back are in bounds
            if sbot <= t and stop >= b and sfront <= d and sback >= f:
                if sleft < l and l <= sright:
                    # print("Left split")
                    doSplit(sl, s, "v", l)
                    delind.append(i)
                    break
                if sleft <= r and r < sright:
                    # print("Right split")
                    doSplit(sl, s, "v", r + 1)
                    delind.append(i)
                    break

            # for efficiency - check left/right and bottom/top are in bounds
            if sleft <= r and sright >= l and sbot <= t and stop >= b:
                if sfront < f and f <= sback:
                    # print("Front split")
                    doSplit(sl, s, "d", f)
                    delind.append(i)
                    break
                if sfront <= d and d < sback:
                    # print("Back split")
                    doSplit(sl, s, "d", d + 1)
                    delind.append(i)
                    break
                pass

        # delete obsolete bounds
        for di in delind:
            sl.pop(di)

        if len(delind) == 0:
            break


def cubesStateChange(sl, action, b, t, l, r, f, d):
    """Toggle on or off the light list items."""

    for s in sl:
        if (
            s[1] >= b
            and s[2] <= t
            and s[3] >= l
            and s[4] <= r
            and s[5] >= f
            and s[6] <= d
        ):
            # print("action", action, "for", s[1:], "is in", b, t, l, r, f, d)

            # only write if necessary
            if action == "on" and s[0] == 0:
                s[0] = 1
            if action == "off" and s[0] == 1:
                s[0] = 0


def getCubesSum(sl):
    """Return the sum of cubes that are on in list."""
    lightsum = 0
    for s in sl:
        if s[0] == 1:
            # HERE - HANDLE NEGATIVE VALUES!
            w = abs(s[4] - s[3]) + 1
            h = abs(s[2] - s[1]) + 1
            d = abs(s[6] - s[5]) + 1
            lightsum += w * h * d
    return lightsum


def loadInput(input_file):
    """Return input data."""
    data = []
    with open(input_file, "r") as fh:
        for line in fh:
            line = line.strip("\n")

            if line == "":
                continue

            if line[0] == "#":
                continue

            cmd = re.match(
                r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)",
                line,
            )
            action = cmd.groups()[0]
            bounds = [int(x) for x in cmd.groups()[1:]]
            data.append([action] + bounds)

    return data


def reboot(data, limit=None):
    """Reboots the core, toggling cubes, returns number on."""
    # determine bounds and create state list
    mbot, mtop, mlft, mrgt, mfrt, mdep = None, None, None, None, None, None
    for ins in data:
        if mbot is None or ins[1] < mbot:
            mbot = ins[1]
        if mtop is None or ins[2] > mtop:
            mtop = ins[2]
        if mlft is None or ins[3] < mlft:
            mlft = ins[3]
        if mrgt is None or ins[4] > mrgt:
            mrgt = ins[4]
        if mfrt is None or ins[5] < mfrt:
            mfrt = ins[5]
        if mdep is None or ins[6] > mdep:
            mdep = ins[6]

    if limit is not None:
        if mbot < -limit:
            mbot = -limit
        if mlft < -limit:
            mlft = -limit
        if mfrt < -limit:
            mfrt = -limit
        if mtop > limit:
            mtop = limit
        if mrgt > limit:
            mrgt = limit
        if mdep > limit:
            mdep = limit

    # set first state and bounds
    sl = [[0, mbot, mtop, mlft, mrgt, mfrt, mdep]]

    for ins in data:
        print("Instruction:", ins)
        # send bounds to split pre-existing volumes
        # * expands into arguments
        cubesSplit(sl, *ins[1:])
        cubesStateChange(sl, *ins)

    # print("Found", getCubesSum(sl), "cubes 'on'")
    return getCubesSum(sl)


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = reboot(data, 50)
    print("Part 1 answer is:", answer)


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    answer = reboot(data)
    print("Part 2 answer is:", answer)


def tests():
    """Check sanity."""
    # Tests
    data = loadInput("test_input")
    assert reboot(data, 50) == 39

    data = loadInput("test_input_larger")
    assert reboot(data, 50) == 590784

    data = loadInput("test_input_p2")
    assert reboot(data, 50) == 474140
    assert reboot(data) == 2758514936282235
    print("All tests passed.")


if __name__ == "__main__":
    # tests()

    data = loadInput("input")
    part1(data)
    part2(data)
