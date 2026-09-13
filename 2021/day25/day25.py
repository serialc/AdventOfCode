"""AoC 2021 - Day 25."""

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

    surf = np.array(data)
    return surf


def cucumber(surf):
    """Count number of steps until cucumber movement locks."""
    h, w = surf.shape

    steps = 0
    while True:
        # cmc.matPrint(surf)
        movement = False

        # make the images
        pixlist = []
        res = 2
        for y in range(h):
            for _ in range(res):
                for x in range(w):
                    for _ in range(res):
                        if surf[y, x] == ">":
                            pixlist.append((100, 255, 100))
                        if surf[y, x] == "v":
                            pixlist.append((255, 100, 100))
                        if surf[y, x] == ".":
                            pixlist.append((100, 100, 100))
        cmc.makeRgbImage(
            pixlist,
            "imgs/" + (3 - len(str(steps))) * "0" + str(steps) + ".png",
            h * res,
            w * res,
        )
        # end of image creation

        # Do it in two waves, East first, then South
        for cudir in [">", "v"]:
            surfcp = np.ndarray(surf.shape, dtype=surf.dtype)
            surfcp[:] = "."

            # Go across entire surface
            for y in range(h):
                for x in range(w):
                    # move sea cucumber to the right
                    if cudir == ">" and surf[y, x] == ">":
                        if x == (w - 1) and surf[y, 0] == ".":
                            surfcp[y, 0] = ">"
                            movement = True
                            continue
                        if x < (w - 1) and surf[y, x + 1] == ".":
                            surfcp[y, x + 1] = ">"
                            movement = True
                            continue
                        surfcp[y, x] = ">"

                    # move sea cucumber down - looking at copied surface
                    if cudir == "v" and surf[y, x] == "v":
                        if y == (h - 1) and surf[0, x] == ".":
                            surfcp[0, x] = "v"
                            movement = True
                            continue
                        if y < (h - 1) and surf[y + 1, x] == ".":
                            surfcp[y + 1, x] = "v"
                            movement = True
                            continue
                        surfcp[y, x] = "v"

            # combine surfaces
            if cudir == ">":
                surfcp[surf == "v"] = "v"
            if cudir == "v":
                surfcp[surf == ">"] = ">"
            # overwrite
            surf = surfcp

        # cmc.matPrint(surfcp)
        steps += 1

        # continue until there's no movement for a cycle
        if not movement:
            break

    print("Flow ended after", steps, "steps")
    return steps


def tests(data):
    """Run some tests."""
    assert cucumber(data) == 58
    print("All tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = cucumber(data)
    print("Part 1 answer is:", answer)


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    answer = cucumber(data)
    print("Part 2 answer is:", answer)


if __name__ == "__main__":
    data = loadInput("input0")
    tests(data)

    data = loadInput("input")
    part1(data.copy())
    # part2(data.copy())
