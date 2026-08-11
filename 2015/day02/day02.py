"""AoC 2015 - Day 2."""

# import numpy as np
# import cmcaoc as cmc

input_file = "input0"
input_file = "input"


paperq = 0
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        w, h, d = [int(x) for x in line.split("x")]

        a = w * h
        b = w * d
        c = h * d

        # which is the smallest
        faces = [a, b, c]
        faces.sort()
        slack = faces[0]

        paperq += 2 * a + 2 * b + 2 * c + slack


print("#### Part 1 ####")
print("Answer is:", paperq)

# PART 2 ####
print("============ Part 2 start ================")

ribbonq = 0
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        w, h, d = [int(x) for x in line.split("x")]

        # which is the smallest
        sides = [w, h, d]
        sides.sort()

        bow = w * h * d
        ribbonq += sides[0] * 2 + sides[1] * 2 + bow

print("#### Part 2 ####")
# 30672640756 is too high - ugh, used areas, not sides
print("Answer is:", ribbonq)
