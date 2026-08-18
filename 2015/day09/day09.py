"""AoC 2015 - Day 9."""

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

            dists = re.match(r"(\w+) to (\w+) = (\d+)", line)

            o, d, dist = dists.groups()
            dist = int(dist)

            if o not in data:
                data[o] = {}
            if d not in data:
                data[d] = {}
            data[o][d] = dist
            data[d][o] = dist

    return data


def solve(data, shortest=True, path=[]):
    """Find the shortest path to visit all points on network."""
    best_path_dist = None
    solve_dist = None

    # go through each node name
    for o in data.keys():

        # only try adding to path unexplored nodes
        if o in path:
            continue

        # add new node to path, and recurse
        solve_dist = solve(data, shortest, path + [o])

        # initialize
        if best_path_dist is None:
            best_path_dist = solve_dist

        # save the shortest path
        if shortest and solve_dist < best_path_dist:
            best_path_dist = solve_dist
        # save the longest path
        if not shortest and solve_dist > best_path_dist:
            best_path_dist = solve_dist

    # if no solve calls were made, because every node is visited
    if solve_dist is None:
        # calculate the path distance
        path_dist = 0
        for i in range(len(path) - 1):
            path_dist += data[path[i]][path[i + 1]]

        # print("Solved path:", path, "distance", str(path_dist))
        return path_dist

    return best_path_dist


def tests(data):
    """Run some tests."""
    assert solve(data) == 605


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")

    print("Part 1 answer is:", solve(data))


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")

    print("Part 2 answer is:", solve(data, shortest=False))


if __name__ == "__main__":
    tdata = loadInput("input0")
    tests(tdata)

    data = loadInput("input")
    part1(data)
    part2(data)
