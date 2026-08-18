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

            # extract values from line
            rel = re.match(
                r"(\w+) can fly (\d+) km\/s for (\d+) seconds, but then must rest for (\d+) seconds.",
                line,
            )

            # clean up values
            rein, spd, dur, rest = rel.groups()
            spd, dur, rest = [int(x) for x in [spd, dur, rest]]

            # insert into data
            data[rein] = {
                "speed": spd,
                "stam": dur,
                "rest": rest,
                "dist": 0,
                "points": 0,
            }
    return data


def race(data, dur):
    """Process reindeer race."""
    time = 0
    while time < dur:
        farthest = 0

        # advance moving reindeer
        for r in data:
            r = data[r]

            # determine if reindeer is currently moving
            if (time % (r["stam"] + r["rest"])) < r["stam"]:
                # add distance travelled
                r["dist"] += r["speed"]

            # determine farthest distance
            if r["dist"] > farthest:
                farthest = r["dist"]

        # give point(s) to the current farthest reindeer
        for r in data:
            if data[r]["dist"] == farthest:
                data[r]["points"] += 1
        time += 1

    # Find the longest distance travelled
    farthest = 0
    for r in data:
        rdist = data[r]["dist"]
        if rdist > farthest:
            farthest = rdist

    # Find the maximum points
    most_points = 0
    for r in data:
        rpoints = data[r]["points"]
        if rpoints > most_points:
            most_points = rpoints

    return {"dist": farthest, "points": most_points}


def tests(data):
    """Run some tests."""
    res = race(data, 1000)
    assert res["dist"] == 1120
    assert res["points"] == 689
    print("All tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")

    answer = race(data, 2503)
    print("Part 1 answer is:", answer["dist"])


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")

    answer = race(data, 2503)
    print("Part 2 answer is:", answer["points"])
    # 22527 - Too high. Used data by reference, than added to first call's travel/points
    #       - Also, loops were embedded in other loop, multiple counting


if __name__ == "__main__":
    tdata = loadInput("input0")
    tests(tdata)

    data = loadInput("input")
    part1(data)
    data = loadInput("input")
    part2(data)
