"""AoC 2015 - Day 24."""

import math

# import re
# import copy
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

            data.append(int(line))
    return data


smallest_size = None


def distribute(gifts, bw, bag=()):
    """Return which number combos reach target bag weight."""
    global smallest_size

    # if bag is good weigh, update shortest if bag is shorter, return bag
    if sum(bag) == bw:
        if smallest_size is None or len(bag) < smallest_size:
            smallest_size = len(bag)
        return [bag]

    # if there are no more gifts and sum(bag) is not target bag weight, return
    if len(gifts) == 0:
        return ()

    # if the bag is already the same size as the smallest found but not a solution, return
    if len(bag) == smallest_size:
        return ()

    blist = []
    # continue exploring combinations
    # -> with next gift
    if (sum(bag) + gifts[0]) <= bw:
        blist += distribute(gifts[1:], bw, bag + (gifts[0],))
    # -> and without next gift
    blist += distribute(gifts[1:], bw, bag)
    return blist


def untangle(data, bags_count=3):
    """Return the entanglement of smallest bag."""
    global smallest_size
    # reset optimization
    smallest_size = None

    # get the target bag weight
    bag_weight = int(sum(data) / bags_count)
    if (sum(data) % bags_count) != 0:
        exit("Unexpected bag weights.")

    # reverse the data [big, ... , small]
    data.sort(reverse=True)
    # THIS, ABOVE, IS THE MOST IMPORTANT PART

    # get all the possible combinations of bags with this weight
    bag_dists = distribute(data, bag_weight)

    smallest = None
    for b in bag_dists:
        if smallest is None or len(b) < smallest:
            smallest = len(b)

    ent_score = []
    for b in bag_dists:
        if len(b) == smallest:
            ent_score.append(math.prod(b))

    return min(ent_score)


def tests(data):
    """Run some tests."""
    assert untangle(data) == 99
    assert untangle(data, 4) == 44
    print("All tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = untangle(data)
    print("Part 1 answer is:", answer)


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    answer = untangle(data, 4)
    print("Part 2 answer is:", answer)


if __name__ == "__main__":
    data = loadInput("input0")
    tests(data)

    data = loadInput("input")
    part1(data)
    part2(data)
