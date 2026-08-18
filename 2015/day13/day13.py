"""AoC 2015 - Day 12."""

# import json
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

            rel = re.match(
                r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.",
                line,
            )
            n1, magn, points, n2 = rel.groups()
            magn = 1 if magn == "gain" else -1
            points = int(points)

            # insert into data
            if n1 not in data:
                data[n1] = {}
            data[n1][n2] = magn * points

    return data


def seatAllocation(data, plan=[]):
    """Allocate people at circular table."""
    guests = list(data.keys())

    # recursion initialization
    if len(plan) == 0:
        # allocate the first guest
        # everything is relative to this
        plan.append(guests[0])

    # recursion closure
    # all allocated, calculate happiness
    if len(plan) == len(guests):
        plan_hap = 0
        for i in range(len(guests)):
            g1 = plan[i - 1]
            g2 = plan[i]
            # add relationship scores, in both directions
            plan_hap += data[g1][g2]
            plan_hap += data[g2][g1]
        return plan_hap

    # recursion branch/merge - select best score
    maxh = None
    for g in guests[1:]:
        if g in plan:
            continue
        hap = seatAllocation(data, plan + [g])
        if maxh is None:
            maxh = hap
        if hap > maxh:
            maxh = hap
    return maxh


def tests(data):
    """Run some tests."""
    assert seatAllocation(data) == 330

    print("All tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")

    answer = seatAllocation(data)

    print("Part 1 answer is:", answer)


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")

    # add "myself" to the seating
    myself = {}
    for g in data:
        myself[g] = 0
        data[g]["myself"] = 0
    data["myself"] = myself

    answer = seatAllocation(data)

    print("Part 2 answer is:", answer)


if __name__ == "__main__":
    tdata = loadInput("input0")
    tests(tdata)

    data = loadInput("input")
    part1(data)
    part2(data)
