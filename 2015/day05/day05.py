"""AoC 2015 - Day 5."""

# import numpy as np
# import cmcaoc as cmc

input_file = "input0"
input_file = "input1"
input_file = "input"


vowels = list("aeiou")

with open(input_file, "r") as fh:

    nicecnt = 0

    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        print(line, ": ", end="")

        # does it have at least 3 vowels
        vcnt = 0
        for v in vowels:
            vcnt += line.count(v)

        if vcnt < 3:
            print("Too few vowels")
            continue

        # twice in a row
        twice = False
        for i in range(len(line) - 1):
            if line[i] == line[i + 1]:
                twice = True
                break

        if not twice:
            print("No doubles")
            continue

        naughtylist = ("ab", "cd", "pq", "xy")
        naughty = False
        for n in naughtylist:
            if n in line:
                print("Bad items")
                naughty = True
                break

        if naughty:
            continue

        # if we reached here, then it's a nice string
        print("Nice")
        nicecnt += 1


print("#### Part 1 ####")
# 260 - too high - the naughty list "continue" was inside another loop!
print("Answer is:", nicecnt)

# PART 2 ####
print("============ Part 2 start ================")


with open(input_file, "r") as fh:

    nicecnt = 0

    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        print(line, ": ", end="")

        # any two letters, twice
        twice = False
        for i in range(len(line) - 3):
            # look for substring
            ss = line[i : i + 2]
            # is there another same double afterwards?
            if ss in line[i + 2 :]:
                twice = True
                break

        if not twice:
            print("No doubles")
            continue

        # same letters, with anything in between
        bookends = False
        for i in range(len(line) - 2):
            if line[i] == line[i + 2]:
                bookends = True
                break

        if not bookends:
            print("No bookends")
            continue

        # if we reached here, then it's a nice string
        print("Nice")
        nicecnt += 1

print("#### Part 2 ####")
print("Answer is:", nicecnt)
