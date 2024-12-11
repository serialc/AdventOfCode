"""
AoC 2024 Day 11.

A doozy, but effective.
Code has extra bits, see the 'count', that didn't serve a purpose.
"""

# import time
# import numpy as np
# import re


def countStoneChildren(stone_map, val, reclimit, recdepth=1):
    """
    Recursively adds the stones based on hierarchy.

    Saves work to not reproduce unnecessary recursion
    """
    global stone_solution

    """Follow dict recursively and count instances."""
    if recdepth == reclimit:
        # return the number of children
        return len(stone_map[val]["maps"])

    # solution code is based on the distance to the reclimit
    solution_code = str(val) + "_" + str(reclimit - recdepth)
    children_sum = 0
    for chval in stone_map[val]["maps"]:

        # use past work if exists
        if solution_code in stone_solution:
            return stone_solution[solution_code]

        children_counts = countStoneChildren(stone_map, chval, reclimit, recdepth + 1)
        children_sum += children_counts

    # save work so we don't do it again
    stone_solution[solution_code] = children_sum
    return children_sum


def buildStoneMap(stone, iterations):
    """
    Create a dict of stone frequencies, and children, then return it.

    A large number (all?) of the stones will follow a similar route
    don't need to calculate a route more than once
    build a conversion map for stone to a count for each iteration
    """
    smap = {}
    stones = [stone]

    for i in range(iterations + 1):
        si = 0
        while si < len(stones):
            if stones[si] in smap:
                smap[stones[si]]["count"] += 1
                del stones[si]
                continue

            if stones[si] == 0:
                stones[si] = 1
                smap[0] = {"maps": [1], "count": 1}
            elif len(str(stones[si])) % 2 == 0:
                slen = int(len(str(stones[si])) / 2)
                sval = stones[si]
                stones[si] = int(str(sval)[:slen])
                stones.insert(si + 1, int(str(sval)[slen:]))
                smap[sval] = {"maps": [stones[si], stones[si + 1]], "count": 1}
                si += 1
            else:
                sval = stones[si]
                stones[si] *= 2024
                smap[sval] = {"maps": [stones[si]], "count": 1}

            si += 1

    # calculate children
    return countStoneChildren(smap, stone, iterations)


input_file = "input0"
input_file = "input"

stones_list = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        stones_list = list(map(int, line.split(" ")))

# save any work done: value, depth
stone_solution = {}  # type: dict[str, int]

iterations = 25
stone_sum = 0
print("Processing stones", stones_list, "for", iterations, "iterations")
for s in stones_list:
    stone_sum += buildStoneMap(s, iterations)

# print(stones)
print("#### Part 1 ####")
print("Answer is:", stone_sum)


# PART 2 ####
print("============ Part 2 start ================")

iterations = 75
stone_sum = 0
print("Processing stones", stones_list, "for", iterations, "iterations")
for s in stones_list:
    stone_sum += buildStoneMap(s, iterations)

print("#### Part 2 ####")
print("Answer is:", stone_sum)
