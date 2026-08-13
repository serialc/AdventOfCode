"""AoC 2015 - Day 4."""

import hashlib

# import numpy as np
# import cmcaoc as cmc

input_file = "input0"
input_file = "input"


with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

# only has one line of data
i = 0
while True:
    hashval = hashlib.md5((line + str(i)).encode("utf-8")).hexdigest()
    if hashval[0:5] == "00000":
        break

    if i % 10000 == 0:
        print(i, hashval)

    i += 1

print("Answer is:", i)

# PART 2 ####
print("============ Part 2 start ================")

# only has one line of data
i = 0
# i = 3682000000
while True:
    hashval = hashlib.md5((line + str(i)).encode("utf-8")).hexdigest()
    if hashval[0:6] == "000000":
        print("Success!", i, hashval)
        break

    if hashval[0:5] == "00000":
        print("Close...", i, hashval)

    i += 1

print("#### Part 2 ####")
print("Answer is:", i)
