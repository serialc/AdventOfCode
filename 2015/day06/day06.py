"""AoC 2015 - Day 6."""

import re

import numpy as np
import cmcaoc as cmc

input_file = "input0"
input_file = "input1"
input_file = "input2"
input_file = "input"

# items structure [on/off, bottom, top, left, right]
ll = []
ls = np.zeros((0, 0))
size = 0


def doSplit(s, horv, val):
    """Split out two areas."""
    global ll

    # print("->", horv, "split", s, "at", val)

    if horv == "h":
        ll.append([s[0], s[1], val - 1, s[3], s[4]])
        ll.append([s[0], val, s[2], s[3], s[4]])

    if horv == "v":
        ll.append([s[0], s[1], s[2], val, s[4]])
        ll.append([s[0], s[1], s[2], s[3], val - 1])


def lightsSplit(b, t, l, r):
    """Divides light list into smaller lists."""
    global ll

    while True:
        # track if we've done splits, delete former bounds
        delind = []

        for i in range(len(ll)):

            s = ll[i]

            # for efficiency
            if s[3] <= r and s[4] >= l:
                if s[1] < b and b <= s[2]:
                    # print("Bottom split")
                    doSplit(s, "h", b)
                    delind.append(i)
                    break
                if s[1] <= t and t < s[2]:
                    # print("Top split")
                    doSplit(s, "h", t + 1)
                    delind.append(i)
                    break
            # for efficiency
            if s[1] <= t and s[2] >= b:
                if s[3] < l and l <= s[4]:
                    # print("Left split")
                    doSplit(s, "v", l)
                    delind.append(i)
                    break
                if s[3] <= r and r < s[4]:
                    # print("Right split")
                    doSplit(s, "v", r + 1)
                    delind.append(i)
                    break

        # delete obsolete bounds
        for di in delind:
            ll.pop(di)

        if len(delind) == 0:
            break


def lightChange(action, b, t, l, r):
    """Toggle on or off the light list items."""
    global ll

    for s in ll:
        if s[1] >= b and s[2] <= t and s[3] >= l and s[4] <= r:
            # print("action", action, "for", s[1:5], "is in", b, t, l, r)

            # change value
            if action == "toggle":
                s[0] = (s[0] + 1) % 2

            # only write if necessary
            if action == "turn on" and s[0] == 0:
                s[0] = 1
            if action == "turn off" and s[0] == 1:
                s[0] = 0


def printList(alist):
    """Print list - one list item per row."""
    for i in alist:
        print(i)


def printLights():
    """Convert list to matrix form for printing."""
    surf = np.zeros((size, size), dtype=np.uint8)

    for i in ll:
        # only turn on the on sections
        if i[0] == 1:
            surf[i[1] : (i[2] + 1), i[3] : (i[4] + 1)] = 1

    # Print matrix in form
    #
    # ^
    # |
    # |
    # 0,0 --->
    (yd, xd) = surf.shape
    for y in range(yd - 1, -1, -1):
        for x in range(xd):
            print(surf[y, x], end="")
        print()


def getLightsSum():
    lightsum = 0
    for s in ll:
        if s[0] == 1:
            w = s[4] - s[3] + 1
            h = s[2] - s[1] + 1
            lightsum += w * h
    return lightsum


with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        if line[0] == "#":
            continue

        if line[0:4] == "size":
            size = int(line.split(" ")[1])

            # Method 1
            # set the starting shape - off
            ll.append([0, 0, size - 1, 0, size - 1])

            # Method 2
            ls = np.zeros((size, size), dtype=np.uint8)
            continue

        # extract the command portions
        cmd = re.match(
            r"(toggle|turn on|turn off) (\d+),(\d+) through (\d+),(\d+)", line
        )
        action = cmd.groups()[0]
        b, l, t, r = [int(x) for x in cmd.groups()[1:]]

        # do the work
        print("Instruction:", line, end="")
        lightsSplit(b, t, l, r)
        lightChange(action, b, t, l, r)
        print(". Resulting list length:", len(ll))

        # printList(ll)
        # printLights()

        # Method 2
        if action == "toggle":
            ls[b : (t + 1), l : (r + 1)] = (ls[b : (t + 1), l : (r + 1)] + 1) % 2
        if action == "turn off":
            ls[b : (t + 1), l : (r + 1)] = 0
        if action == "turn on":
            ls[b : (t + 1), l : (r + 1)] = 1
        # cmc.matPrint(ls)

        if ls.sum() != getLightsSum():
            print("Matrix sum:", ls.sum())
            print("List sum:", getLightsSum())
            exit("Error - inconsistent light sum")


print("#### Part 1 ####")
print("Answer is:", getLightsSum(), ls.sum())
# 438822 - Too high: Updated action label from "on" to "turn on" and forgot
#        - Also, for "turn off" was checking wrong index!

# PART 2 ####
print("============ Part 2 start ================")

with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        if line[0] == "#":
            continue

        if line[0:4] == "size":
            size = int(line.split(" ")[1])

            # Method 2
            ls = np.zeros((size, size), dtype=np.uint8)
            continue

        # extract the command portions
        cmd = re.match(
            r"(toggle|turn on|turn off) (\d+),(\d+) through (\d+),(\d+)", line
        )
        action = cmd.groups()[0]
        b, l, t, r = [int(x) for x in cmd.groups()[1:]]

        if action == "toggle":
            ls[b : (t + 1), l : (r + 1)] += 2
        if action == "turn off":
            # Aaaah, (0 - 1) -> 255! Carefull!
            offcan = ls[b : (t + 1), l : (r + 1)]
            offcan[offcan > 0] -= 1
        if action == "turn on":
            ls[b : (t + 1), l : (r + 1)] += 1

print("#### Part 2 ####")
print("Answer is:", ls.sum())
# 19700307 - Too high. Looping from (0 - 1) to 255, gave us too high values
