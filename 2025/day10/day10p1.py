"""AoC 2025 Day 10 part 1."""

import sys
import numpy as np
import re

# import time
# import functools  # for memoization

# import math
# from PIL import Image

# get input file from command line
input_file = "input"
if len(sys.argv) == 2:
    input_file += sys.argv[1]
print("\nProcessing input file:", input_file)


def rsearch(goal, state, depth, bset, pressedset):
    """Return button presses that turn on correct pattern."""
    if state == goal:
        return len(pressedset)

    # we've pressed each button once - and not gotten the answer -> failed
    if depth == len(bset):
        return np.inf

    # can only press each button a maximum of one time
    bs = bset[depth]

    # don't press this button
    score1 = rsearch(goal, state.copy(), depth + 1, bset, pressedset)

    # do press this button
    tstate = state.copy()
    # combos have 1 or more buttons
    for b in bs:
        tstate[b] ^= 1
    score2 = rsearch(goal, tstate, depth + 1, bset, pressedset + [depth])

    if score1 < score2:
        return score1
    return score2


results = []
with open(input_file, "r") as fh:
    step = 0
    for line in fh:
        line = line.strip("\n")

        char_lights = re.findall(r"\[(.+)\]", line)[0]
        digit_lights = char_lights.replace(".", "0").replace("#", "1")
        lights = [int(x) for x in list(digit_lights)]
        # print("Goal", lights, end="")

        bcl = re.findall(r"\] (.+) \{", line)
        bcl2 = bcl[0].replace("(", "").replace(")", "").split(" ")
        bcombs = [[int(y) for y in x.split(",")] for x in bcl2]
        # print("Button connections", bcombs)

        # send goal, off state, btn connections, btn presses
        res = rsearch(lights, [0] * len(lights), 0, bcombs, [])
        results.append(res)
        # print("Button presses", res)

# print(results)
print("#### Part 1 ####")
print("Answer is:", sum(results))
