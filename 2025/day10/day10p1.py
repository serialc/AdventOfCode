"""AoC 2025 Day 10 part 1."""

import sys
import numpy as np
import re
import time
import functools  # for memoization

# import math
# from PIL import Image

# get input file from command line
input_file = "input"
if len(sys.argv) == 2:
    input_file += sys.argv[1]
print("\nProcessing input file:", input_file)

lights = []
bcombs = []
with open(input_file, "r") as fh:
    step = 0
    for line in fh:
        line = line.strip("\n")

        lights.append(re.findall(r"\[(.+)\]", line)[0])
        bcl = re.findall(r"\] (.+) \{", line)
        bcl2 = bcl[0].replace("(", "").replace(")", "").split(" ")
        bcombs.append([[int(y) for y in x.split(",")] for x in bcl2])


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

        # can only press each button a maximum of one time
        if bs in pressedset:
            continue

        tstate = state.copy()
        # combos have 1 or more buttons
        for b in bs:
            if tstate[b] == ".":
                tstate[b] = "#"
            else:
                tstate[b] = "."

        # print(" " * len(pressedset), tstate)

        score = rsearch(goal, tstate, bset, pressedset + [bs])
        if score is not False and score < lowest:
            lowest = score

    return lowest


results = []
for i in range(len(lights)):
    print("Searching:", lights[i], "Sum: ", end="")
    res = rsearch(list(lights[i]), list("." * len(lights[i])), bcombs[i], [])
    results.append(res)
    print(res, "Current sum:", sum(results))

# print(results)
print("#### Part 1 ####")
print("Answer is:", sum(results))
