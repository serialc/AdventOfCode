"""AoC 2024 Day 8."""

# import numpy as np
# import re

input_file = "input0"
input_file = "input"

disc = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        fs = list(map(int, list(line)))

        is_file = True
        fid = 0
        for f in fs:
            if is_file:
                disc.extend([str(fid)] * f)
                fid += 1
            else:
                disc.extend(["."] * f)
            is_file = not is_file

# print(disc)
while "." in disc:
    # get first empty space replace with last character
    # assumes there is no '.' at the end
    i = disc.index(".")
    disc[i] = disc.pop()
    # print(disc)

# calculate hash
hashval = 0
for i in range(len(disc)):
    hashval += i * int(disc[i])


print("#### Part 1 ####")
print("Answer is:", hashval)
# takes about 10 seconds... a bit long


# PART 2 ####
print("============ Part 2 start ================")


def printDisc():
    """Print disc contents."""
    for f in disc:
        if f["t"] == "f":
            print(str(f["fid"]) * f["size"], end="")
        else:
            print("." * f["size"], end="")
    print()


disc = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        fs = list(map(int, list(line)))

        is_file = True
        fid = 0
        for f in fs:
            if is_file:
                disc.append({"t": "f", "size": f, "fid": fid})
                fid += 1
            else:
                disc.append({"t": "s", "size": f})
            is_file = not is_file


# printDisc()

# compress
back_task = len(fs) - 1
while back_task > 0:
    space_seek = 0

    # if pointing at file
    if disc[back_task]["t"] == "f":

        fsize = disc[back_task]["size"]

        # look for all available spots
        while space_seek != back_task:

            if disc[space_seek]["t"] == "s" and disc[space_seek]["size"] >= fsize:

                # take out the file now before we change index values
                moving_file = disc.pop(back_task)
                # replace with a blank space of the same size
                disc.insert(back_task, {"t": "s", "size": moving_file["size"]})

                # adjust the space, either del or reduce
                if disc[space_seek]["size"] == fsize:
                    del disc[space_seek]
                else:
                    disc[space_seek]["size"] -= fsize

                # now move the task (otherwise indexing would change)
                disc.insert(space_seek, moving_file)

                # now jump to next task
                break

            # look for first space
            while disc[space_seek]["t"] != "s" or disc[space_seek]["size"] < fsize:
                space_seek += 1

                # if we didn't find one to the left of current position
                # stop searching
                if space_seek == back_task:
                    break

    # need to point back task at a correct value
    back_task -= 1
    while disc[back_task]["t"] != "f":
        back_task -= 1

# calculate hash
hashval = 0
pos = 0
for i in range(len(disc)):

    if disc[i]["t"] == "f":
        hashval += sum(
            [disc[i]["fid"] * pv for pv in range(pos, pos + disc[i]["size"])]
        )

    pos += disc[i]["size"]

print("#### Part 2 ####")
print("Answer is:", hashval)
