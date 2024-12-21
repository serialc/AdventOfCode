"""AoC 2024 Day 20."""

import numpy as np
import functools

# import sys
# sys.setrecursionlimit(40000)
# import time
# import re


def branchSearch(pat, twls):
    # print(pat)
    if len(pat) == 0:
        return True

    for t in twls:
        # print(t, pat[: len(t)], pat[: len(t)] == t)
        if pat[: len(t)] == t:
            # print(t, "match")
            if branchSearch(pat[len(t) :], twls):
                return True

    return False


input_file = "input0"
input_file = "input"
twls = []
vpats = 0
with open(input_file, "r") as fh:
    towels = True
    for line in fh:
        line = line.strip("\n")

        if towels:
            twls = line.split(", ")
            towels = False
            continue

        if line == "":
            continue

        pat = line

        if branchSearch(pat, twls):
            vpats += 1


print("#### Part 1 ####")
print("Answer is:", vpats)


# PART 2 ####
print("============ Part 2 start ================")


# memoization!
@functools.cache
def branchSearchSum(pat):
    """See which towels function for this desired pattern start."""
    if len(pat) == 0:
        # print()
        return 1

    combsum = 0
    for t in twls:
        if pat[: len(t)] == t:
            # print(t, " ", end="")
            combsum += branchSearchSum(pat[len(t) :])

    return combsum


twls = []
vpats = 0
with open(input_file, "r") as fh:
    towels = True
    for line in fh:
        line = line.strip("\n")

        if towels:
            twls = line.split(", ")
            towels = False
            continue

        if line == "":
            continue

        pat = line

        print("Solve", pat)
        vpats += branchSearchSum(pat)
        # print()

print("#### Part 2 ####")
print("Answer is:", vpats)
# 690 - too low: Wasn't calling new function recursively
# 643685981770598 - memoization to the rescue.
