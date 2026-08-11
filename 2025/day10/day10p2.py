"""AoC 2025 Day 10 part 2."""

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


def getListDepth(L):
    """Return the list depth."""
    if isinstance(L, list):
        if len(L) == 0:
            return 1
        return max(map(getListDepth, L)) + 1
    else:
        return False


def getSolutionClickSets(goal, state, depth, bset, pressedset):
    """Return button presses that turn on correct pattern."""
    if depth == len(bset):
        if state == goal:
            return pressedset
        # we've reach the permutation end
        return False

    # can only press each button a maximum of one time
    bs = bset[depth]

    # don't press this button
    set1 = getSolutionClickSets(goal, state.copy(), depth + 1, bset, pressedset)

    # do press this button
    tstate = state.copy()
    # combos have 1 or more buttons
    for b in bs:
        tstate[b] ^= 1
    set2 = getSolutionClickSets(goal, tstate, depth + 1, bset, pressedset + [depth])

    # print("sets", set1, set2)
    if set1 is not False and set2 is not False:

        # don't want list nesting
        if getListDepth(set1) > 1 and getListDepth(set2) > 1:
            return set1 + set2
        if getListDepth(set1) > 1:
            return set1 + [set2]
        if getListDepth(set2) > 1:
            return [set1] + set2
        return [set1, set2]

    if set1 is not False:
        if getListDepth(set1) == 1:
            # need some nesting
            return [set1]
        else:
            return set1

    if set2 is not False:
        if getListDepth(set2) == 1:
            # need some nesting
            return [set2]
        else:
            return set2

    return False


def solveFill(jolts, bcombs, depth=0, debug=False):
    """Recurse to simplify problem."""
    mar = " " * depth * 2

    if debug:
        print(mar, "solveFill(", jolts, ") at depth", depth)

    # get the uneven jolts
    jodd = [x % 2 for x in jolts]

    if debug:
        print(mar, "Target changes", jodd)
    # find all the button click sets that can generate this
    success_sets = getSolutionClickSets(jodd, [0] * len(jolts), 0, bcombs, [])

    if success_sets is False:
        if debug:
            print(mar, "Return - No solution found")
        return False

    if len(success_sets) == 0:
        quit("Starting state is all even. This should never happen")

    if getListDepth(success_sets) != 2:
        print("BAD FORM", success_sets)
        quit("List depth should always be 2")

    if debug:
        print(mar, "Successful sets", success_sets)

    best = np.inf
    # Now we need to implement each set of button clicks
    # differing (even) joltages will result
    for sset in success_sets:

        # Calculate the new jolt values on copy
        new_jolts = np.array(jolts.copy(), dtype=int)

        # for each button in this successful set, reduce jolts accordingly
        for b in sset:
            # look at the jolt connections for this button
            for j in bcombs[b]:
                new_jolts[j] -= 1
        if debug:
            print(mar, "Used the set", sset, "to resolve jolts to", new_jolts)

        # check if we're finished
        if np.any(new_jolts < 0):
            if debug:
                print(
                    mar,
                    "Return - Solution using",
                    sset,
                    "has negative jolts",
                    new_jolts,
                )
            continue

        if sum(new_jolts) == 0:
            # if so save the smallest number of clicks to do so
            if len(sset) < best:
                best = len(sset)
                if debug:
                    print(
                        mar,
                        "Continue - Solved using",
                        sset,
                        "of",
                        len(sset),
                        "clicks",
                    )
            continue

        # if not finished simplify
        # divide by two (or a power)
        mult = 2
        while True:
            half_jolts = np.array(new_jolts / mult, dtype=int)
            if (half_jolts % 2 == 0).all():
                mult *= 2
            else:
                break

        # convert back to list
        half_jolts = half_jolts.tolist()
        if debug:
            print(
                mar,
                "Divided remaining (",
                new_jolts,
                ") to ",
                half_jolts,
            )

        bclicks = solveFill(half_jolts, bcombs, depth + 1, debug=debug)

        if bclicks is not False and bclicks != np.inf:
            sclicks = len(sset) + mult * bclicks
            if sclicks < best:
                if debug:
                    print(
                        mar,
                        "Save best to date",
                        len(sset),
                        "+",
                        mult,
                        "*",
                        bclicks,
                    )
                best = sclicks
            else:
                if debug:
                    print(mar, "Don't save", best, "<=", sclicks)

    if debug:
        print(mar, "Return - Lowest clicks found", best)
    return best


# followed @tenchmascot's algorithm (without caching)
# https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
clickslist = []
with open(input_file, "r") as fh:
    linecount = 0
    for line in fh:
        line = line.strip("\n")

        linecount += 1

        debug = False

        bcl = re.findall(r"\] (.+) \{", line)
        bcl2 = bcl[0].replace("(", "").replace(")", "").split(" ")
        bcombs = [[int(y) for y in x.split(",")] for x in bcl2]
        # print("Button connections", bcombs)

        char_jolts = re.findall(r"\{(.+)\}", line)[0].split(",")
        jolts = [int(x) for x in char_jolts]
        print(linecount, "Solve click count for jolts", jolts, "with", bcombs)

        mult = 1
        if False:
            # check if the jolts are all even
            half_jolts = np.array(jolts, dtype=int)
            while True:
                # if jolts cleanly divisible by 2
                if (half_jolts % 2 == 0).all():
                    half_jolts = np.array(half_jolts / 2, dtype=int)
                    mult *= 2
                    jolts = half_jolts.tolist()
                    print("Special - Halved at start", jolts)
                else:
                    break

        clicks = solveFill(jolts, bcombs, debug=debug) * mult

        if clicks == np.inf:
            print("Failed - Did not solve jolts", jolts)
            continue

        print(linecount, "Solved with", clicks, "clicks")

        clickslist.append(clicks)

print(clickslist)
print("#### Part 2 ####")
print("Answer is:", sum(clickslist))
print("Expected answer is", 17214)
