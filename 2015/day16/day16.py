"""AoC 2015 - Day 16."""

import re

# import json
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

            # Sue 1: children: 1, cars: 8, vizslas: 7
            res = re.match(
                r"Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)",
                line,
            )

            # extract and clean up
            sid, l1, q1, l2, q2, l3, q3 = res.groups()
            sid, q1, q2, q3 = [int(x) for x in [sid, q1, q2, q3]]

            data[sid] = {l1: q1, l2: q2, l3: q3}
    return data


def sueMatch(data, req, updated=False):
    """Return the sid of the matching Sue."""

    for sid in data:
        sue = data[sid]

        match_count = 0
        for lbl in sue.keys():

            # updated rules
            if updated and lbl in ["cats", "trees", "pomeranians", "goldfish"]:
                if lbl in ["cats", "trees"]:
                    if req[lbl] < sue[lbl]:
                        match_count += 1

                if lbl in ["pomeranians", "goldfish"]:
                    if req[lbl] > sue[lbl]:
                        match_count += 1
                continue

            # basic rules
            if req[lbl] == sue[lbl]:
                match_count += 1

        if match_count == 3:
            return sid


def tests(data):
    """Run some tests."""
    print("All tests passed!")


def part1(data, req):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = sueMatch(data, req)
    print("Part 1 answer is:", answer)


def part2(data, req):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    answer = sueMatch(data, req, True)
    print("Part 2 answer is:", answer)


if __name__ == "__main__":
    # tdata = loadInput("input0")
    # tests(tdata)
    req = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    data = loadInput("input")
    part1(data, req)
    part2(data, req)
