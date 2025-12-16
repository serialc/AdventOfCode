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


def rsearch(goal, state, bset, pressedset):
    """Return button presses that turn on correct pattern."""
    if state == goal:
        return len(pressedset)

    # we've pressed each button once - failed
    if len(pressedset) == len(bset):
        return False

    # do each button press combo
    lowest = np.inf

    # line below is key! only search a subset as we go deeper into recursion!
    for bs in bset[len(pressedset) :]:

        # !! can only press each button a maximum of one time
        if bs in pressedset:
            continue

        tstate = state.copy()
        # combos have 1 or more buttons
        for b in bs:
            tstate[b] ^= 1

        score = rsearch(goal, tstate, bset, pressedset + [bs])

        if score is not False and score < lowest:
            lowest = score

    return lowest


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
        res = rsearch(lights, [0] * len(lights), bcombs, [])
        results.append(res)
        # print("Button presses", res)

# print(results)
print("#### Part 1 ####")
print("Answer is:", sum(results))
