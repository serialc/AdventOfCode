"""AoC 2015 - Day 18."""

import numpy as np
import cmcaoc as cmc

# import re
# import json
# import functools  # for memoization


def loadInput(input_file):
    """Return input data."""
    data = []
    with open(input_file, "r") as fh:
        for line in fh:
            line = line.strip("\n")

            if line == "":
                continue

            data.append(list(line))

    surf = np.array((np.array(data) == "#") * 1, dtype=np.uint8)
    return surf


def flicker(data, count, corner=False):
    """Implement cellular automata."""
    # turn on corner lights, if required
    if corner:
        cornerLights(data)

    h, w = data.shape
    # number of iterations
    for i in range(count):

        # use temporary surface to write new states to
        surf = data.copy()

        # go through each cell in surface
        for y in range(h):
            for x in range(w):

                # define neighbourhood bounds
                top = 0 if y == 0 else y - 1
                bot = h if y == (h - 1) else y + 2
                left = 0 if x == 0 else x - 1
                right = w if x == (w - 1) else x + 2

                # get neighbours (and cell in centre)
                ln = data[top:bot, left:right]

                # turn off light if not 2-3 neighbours on
                if data[y, x] == 1 and ln.sum() not in [3, 4]:
                    surf[y, x] = 0

                # turn on if exactly 3 neighbours on
                if data[y, x] == 0 and ln.sum() == 3:
                    surf[y, x] = 1

        # overwrite last state
        data = surf
        # cmc.matPrint(data)

        # turn on corner lights, if required
        if corner:
            cornerLights(data)

        # generate image
        if w == 100:
            pl = cmc.makePixelListHw(data, scale=True, res=4)
            pi = (4 - len(str(i))) * "0" + str(i)
            cmc.makeRgbImage(
                pl["pixlist"],
                "gif/" + str(corner) + "_ca_" + pi + ".png",
                pl["h"],
                pl["w"],
            )

    print("Lights on", data.sum())
    return data.sum()


def cornerLights(data):
    """Turn on lights in corners."""
    h, w = data.shape
    data[0, 0] = 1
    data[h - 1, 0] = 1
    data[0, w - 1] = 1
    data[h - 1, w - 1] = 1


def tests(data):
    """Run some tests."""
    assert flicker(data.copy(), 4) == 4
    assert flicker(data.copy(), 5, True) == 17
    print("All tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = flicker(data, 100)
    print("Part 1 answer is:", answer)


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    # turn on corner lights
    answer = flicker(data, 100, True)
    print("Part 2 answer is:", answer)


if __name__ == "__main__":
    data = loadInput("input0")
    tests(data)

    data = loadInput("input")
    part1(data.copy())
    part2(data.copy())
