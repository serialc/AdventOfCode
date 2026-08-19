"""AoC 2015 - Day 3."""

# import numpy as np
# import cmcaoc as cmc

input_file = "input0"
input_file = "input"


with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

# only one line
x = 0
y = 0
locs = {}
for d in line:
    loc = (x, y)
    if loc not in locs:
        locs[loc] = True

    if d == ">":
        x += 1
    if d == "<":
        x -= 1
    if d == "^":
        y += 1
    if d == "v":
        y -= 1

print("#### Part 1 ####")
print("Answer is:", len(locs))

# PART 2 ####
print("============ Part 2 start ================")

locs = {}
sx, sy = (0, 0)
bx, by = (0, 0)

sloc = (sx, sy)
bloc = (bx, by)

if sloc not in locs:
    locs[sloc] = True
if bloc not in locs:
    locs[bloc] = True

insfor = "santa"
for d in line:

    # alternate instructions
    if insfor == "santa":
        if d == ">":
            sx += 1
        if d == "<":
            sx -= 1
        if d == "^":
            sy += 1
        if d == "v":
            sy -= 1
        insfor = "bot"
    else:
        if d == ">":
            bx += 1
        if d == "<":
            bx -= 1
        if d == "^":
            by += 1
        if d == "v":
            by -= 1
        insfor = "santa"

    sloc = (sx, sy)
    bloc = (bx, by)

    if sloc not in locs:
        locs[sloc] = True
    if bloc not in locs:
        locs[bloc] = True

print("#### Part 2 ####")
print("Answer is:", len(locs))
