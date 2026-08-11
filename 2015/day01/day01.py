"""AoC 2015 - Day 1."""

# import numpy as np
# import cmcaoc as cmc

input_file = "input0"
input_file = "input"


with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

# file only has one line, split it up into characters
up = line.count("(")
down = line.count(")")

print("#### Part 1 ####")
print("Answer is:", up - down)

# PART 2 ####
print("============ Part 2 start ================")

floor = 0
for i in range(len(line)):
    c = line[i]
    if c == "(":
        floor += 1
    if c == ")":
        floor -= 1
    if floor < 0:
        break

print("#### Part 2 ####")
print("Answer is:", i + 1)
