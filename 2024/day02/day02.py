"""AoC 2024 - Day 2."""

import numpy as np

input_file = "input0"
input_file = "input"

safecount = 0
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        lvls = np.array(list(map(int, line.split())))
        diffs = np.diff(lvls)

        if (np.all(diffs > 0) or np.all(diffs < 0)) and np.all(np.abs(diffs) <= 3):
            safecount += 1

print("#### Part 1 ####")
print("Answer is:", safecount)

# PART 2 ####
print("============ Part 2 start ================")

safecount = 0
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        lvls = np.array(list(map(int, line.split())))
        diffs = np.diff(lvls)

        if (np.all(diffs > 0) or np.all(diffs < 0)) and np.all(np.abs(diffs) <= 3):
            safecount += 1
            continue

        # can we make the report safe?
        # try removing each one and see
        for i in range(len(lvls)):
            sublvls = np.delete(lvls, i)
            diffs = np.diff(sublvls)
            if (np.all(diffs > 0) or np.all(diffs < 0)) and np.all(np.abs(diffs) <= 3):
                safecount += 1
                break

print("#### Part 2 ####")
print("Answer is:", safecount)
