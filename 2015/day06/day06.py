"""AoC 2015 - Day 6."""

# import numpy as np
# import cmcaoc as cmc

input_file = "input0"
# input_file = "input"

# items structure [on/off, bottom, left, top, right]
ll = [[0, 0, 0, 999, 999]]


def doSplit(s, horv, val, special=False):
    global ll

    print("doSplit", s, horv, val)
    if horv == "h":
        ll.append([s[0], s[1], s[2], val - 1, s[4]])
        ll.append([s[0], val, s[2], s[3], s[4]])

    if horv == "v":
        ll.append([s[0], s[1], s[2], s[3], val - 1])
        ll.append([s[0], s[1], val, s[3], s[4]])


def lightsSplit(b, l, t, r):
    """Divides light list into smaller lists."""
    global ll

    while True:
        # track if we've done splits, delete former bounds
        delind = []

        for i in range(len(ll)):

            s = ll[i]
            print(s)

            if s[1] < b and b < s[3]:
                doSplit(s, "h", b)
                delind.append(i)
                break
            if s[1] < t and t < s[3]:
                doSplit(s, "h", t + 1)
                delind.append(i)
                break
            if s[2] < l and l < s[4]:
                doSplit(s, "v", l)
                delind.append(i)
                break
            if s[2] < r and r < s[4]:
                doSplit(s, "v", r + 1)
                delind.append(i)
                break

        for di in delind:
            ll.pop(di)

        if len(delind) == 0:
            break


def lightChange(action, b, l, t, r):
    """Toggle on or off the light list items."""
    global ll

    for s in ll:
        if s[1] == b and s[2] == l and s[3] == t and s[4] == r:
            if action == "toggle":
                print("OKAY")
                if s[0] == 0:
                    action = "on"
                else:
                    action = "off"
            if action == "on":
                s[0] = 1
            if action == "off":
                s[0] = 0


def printList(alist):
    """Print list - one list item per row."""
    for i in alist:
        print(i)


with open(input_file, "r") as fh:

    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        parts = line.split(" ")

        if len(parts) == 4:
            action = "toggle"
            blc = [int(x) for x in parts[1].split(",")]
            trc = [int(x) for x in parts[3].split(",")]
        else:
            action = parts[1]
            blc = [int(x) for x in parts[2].split(",")]
            trc = [int(x) for x in parts[4].split(",")]

        # unpack the coordinate arguements
        lightsSplit(*blc, *trc)
        lightChange(action, *blc, *trc)
        break

lightsum = 0
for s in ll:
    if s[0] == 1:
        w = s[4] - s[2] + 1
        h = s[3] - s[1] + 1
        lightsum += w * h

print("#### Part 1 ####")
print("Answer is:", lightsum)

# PART 2 ####
print("============ Part 2 start ================")


print("#### Part 2 ####")
print("Answer is:", 0)
