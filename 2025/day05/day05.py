"""AoC 2025 Day 05."""

# import numpy as np
# from PIL import Image
# import sys
# import time
# import re

input_file = "input0"
input_file = "input1"
input_file = "input"

count = 0
rules = []
with open(input_file, "r") as fh:
    step = 0
    for line in fh:
        line = line.strip("\n")

        if line == "":
            step = 1
            continue

        if step == 0:
            low, high = [int(x) for x in line.split("-")]
            rules.append([low, high])

        if step == 1:
            num = int(line)
            for rule in rules:
                if num >= rule[0] and num <= rule[1]:
                    # print(num, "is fresh")
                    count += 1
                    break

print("#### Part 1 ####")
print("Answer is:", count)


# PART 2 ####
print("============ Part 2 start ================")

# dict rules - get the low
drules = {}

# let's sort the rules
for rule in rules:
    # this killed me
    # I didn't consider there might be duplicates!
    if rule[0] in drules:
        print("Doing iffy stuff here", rule[0])
        drules[rule[0] + 1] = rule
        continue
    drules[rule[0]] = rule

# sort the keys
dkeys = list(drules.keys())
dkeys.sort()

# make sure our rule sets are the same length
# as this wasn't the case for a while
if len(drules) != len(rules):
    quit("We have a problem!")

lastmax = 0
count = 0
for dkey in dkeys:
    low, high = drules[dkey]
    print("LH:", low, high, "LM", lastmax, "Count=", count)

    if low > lastmax:
        print("L>LM", low, "-", high, "Added:", high - low + 1)
        count += high - low + 1
        lastmax = high
        continue

    if high <= lastmax:
        print("Nothing added")
        continue

    if low <= lastmax:
        print("L<=LM", lastmax + 1, "-", high, "Added:", high - lastmax)
        count += high - lastmax
        lastmax = high
        continue

    quit("Unexpected situation")

# 431481280987232 is too high - obviously range duplicates
# 324257592789071 is too low - why did I submit this?
# 316924510848106 is too low - stupid - need to go up!
print("#### Part 2 ####")
print("Answer is:", count)
