"""AoC 2015 - Day 17."""

# import re
# import json
# import numpy as np
# import cmcaoc as cmc
# import functools  # for memoization


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

            data.append(int(line))

    return data


def fill(data, vol, cont=[], depth=0):
    """Return the number of permutations that can contain a specific volume."""
    # Recursion end
    if sum(cont) == vol:
        return 1
    if sum(cont) > vol:
        return 0
    # failed to attain volume
    if depth >= len(data):
        return 0

    # Recursion branching
    combinations = 0
    # Use this container or don't
    combinations += fill(data, vol, cont + [data[depth]], depth + 1)
    combinations += fill(data, vol, cont, depth + 1)

    return combinations


def minFill(data, vol, cont=[], depth=0):
    """Return the number of container permutations that can contain a specific volume."""
    # Recursion end, return a list
    if sum(cont) == vol:
        return [len(cont)]
    if sum(cont) > vol:
        return []
    # failed to attain volume
    if depth >= len(data):
        return []

    # Recursion branching
    solutions = []
    # Use this container or don't
    solutions += minFill(data, vol, cont + [data[depth]], depth + 1)
    solutions += minFill(data, vol, cont, depth + 1)

    return solutions


def tests(data, vol):
    """Run some tests."""
    assert fill(data, vol) == 4

    reslist = minFill(data, vol)
    assert reslist.count(min(reslist)) == 3
    print("All tests passed!")


def part1(data, vol):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = fill(data, vol)
    print("Part 1 answer is:", answer)


def part2(data, vol):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    combinations = minFill(data, vol)
    print("Part 2 answer is:", combinations.count(min(combinations)))


if __name__ == "__main__":
    data = loadInput("input0")
    tests(data, 25)

    data = loadInput("input")
    part1(data, 150)
    part2(data, 150)
