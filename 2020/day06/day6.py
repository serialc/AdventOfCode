import numpy as np
import re

cumsum = 0
gdict = {}
with open('input.txt', 'r') as fh:
    for line in fh:

        line = line.rstrip()

        # end of goup
        if line == "":
            cumsum += len(gdict)

            # reset for next group
            gdict = {}
            continue

        for char in line:
            gdict[char] = 0

# catch last group
cumsum += len(gdict)

# Part 1
print("Part 1 - sum of groups: " + str(cumsum))

cumsum = 0
gdict = {}
gcount = 0
with open('data/day6/input.txt', 'r') as fh:
    for line in fh:

        line = line.rstrip()

        # end of goup
        if line == "":
            for char in gdict:
                if gdict[char] == gcount:
                    cumsum += 1

            # reset for next group
            gdict = {}
            gcount = 0
            continue

        gcount += 1
        for char in line:
            if char in gdict:
                gdict[char] += 1
            else:
                gdict[char] = 1


# catch last group
for char in gdict:
    if gdict[char] == gcount:
        cumsum += 1

# Part 2
print("Part 2 - sum of groups: " + str(cumsum))
