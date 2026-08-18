"""AoC 2015 - Day 10."""

import re

# import numpy as np
# import cmcaoc as cmc
# import functools  # for memoization


def loadInput(input_file):
    """Return input data."""
    data = {}
    with open(input_file, "r") as fh:
        for line in fh:
            line = line.strip("\n")

            if line == "":
                continue

            if line[0] == "#":
                continue

            if line[0:4] == "iter":
                data["iter"] = int(line.split("=")[1])
                continue
            if line[0:6] == "answer":
                data["answer"] = line.split("=")[1]
                continue
            data["input"] = line

    return data


def solve(digs, iterations):
    """Read out the digits, and then recurse."""
    if iterations == 0:
        return len(digs)

    # split digs by reoccuring digits
    diglist = []
    ldig = None
    cdig = 0
    for d in list(digs):
        if ldig is None:
            ldig = d
            cdig = 1
            continue

        if ldig != d:
            # add to list
            diglist.append(ldig * cdig)
            ldig = d
            cdig = 1
            continue

        cdig += 1

    # repeat at end, for unprocessed characters
    diglist.append(ldig * cdig)

    # build new string
    nstr = ""
    for ds in diglist:
        nstr += str(len(ds)) + str(ds[0])

    return solve(nstr, iterations - 1)


def tests(data):
    """Run some tests."""
    assert solve(data["input"], data["iter"]) == len(data["answer"])
    print("All tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")

    print("Part 1 answer is:", solve(data["input"], data["iter"]))


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")

    print("Part 2 answer is:", solve(data["input"], 50))


if __name__ == "__main__":
    tdata = loadInput("input0")
    tests(tdata)

    data = loadInput("input")
    part1(data)
    part2(data)
