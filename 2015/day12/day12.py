"""AoC 2015 - Day 12."""

import json

# import re
# import numpy as np
# import cmcaoc as cmc
# import functools  # for memoization


def loadInput(input_file):
    """Return input data."""
    with open(input_file, "r") as fh:
        return json.load(fh)


def sumJsonNumbers(data, no_red=False):
    """Sum all numbers found in JSON."""

    numsum = 0

    if type(data) not in [int, list, dict, str]:
        exit("Unexpected item of type " + str(type(data)))

    if type(data) is int:
        return data

    if type(data) is str:
        return 0

    if type(data) is list:
        for item in data:
            if type(item) is int:
                numsum += item
            else:
                numsum += sumJsonNumbers(item, no_red)

    if type(data) is dict:

        # check dict for "red" values, ignore if found
        if no_red and "red" in list(data.values()):
            # skip children
            return numsum

        for k in data.keys():
            numsum += sumJsonNumbers(data[k], no_red)

    return numsum


def tests(data):
    """Run some tests."""
    assert sumJsonNumbers(data[0]) == 3
    assert sumJsonNumbers(data) == 9
    assert sumJsonNumbers(data[1], no_red=True) == 4
    assert sumJsonNumbers(data, no_red=True) == 7

    print("All tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")

    print("Part 1 answer is:", sumJsonNumbers(data))


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")

    print("Part 2 answer is:", sumJsonNumbers(data, no_red=True))


if __name__ == "__main__":
    tdata = loadInput("input0")
    tests(tdata)

    data = loadInput("input")
    part1(data)
    part2(data)
