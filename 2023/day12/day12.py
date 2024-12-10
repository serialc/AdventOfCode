"""AoC 2023 - Day 12 solving."""

import numpy as np

# from PIL import Image
# import re
# import sys
import math


# combinations calculation - see Pascale's triangle
def nChooseK(n, k):
    """Calculate possible combinations."""
    return math.factorial(n) / math.factorial(n - k) / math.factorial(k)


input_file = "input0"
input_file = "input"

tot_posib = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        # operational '.' or damaged '#' springs
        # ? unknown, numbers indicate contiguous '#'
        # ???.### 1,1,3
        row, recstr = line.split(" ")
        rec = list(map(int, recstr.split(",")))

        # print("raw:", row, rec)

        posib = 1

        # let's try to simplify things
        # repeat until I can't do this anymore
        while True:
            rlen = len(row)

            # if there's still some row, but no records, then empty row
            if len(rec) == 0:
                row = ""

            # if there are any '.' (operational spring) on either end,
            # remove them
            row = row.rstrip(".").lstrip(".")

            # if the first or last are '#' we can remove the known number
            # of contiguous broken springs plus an operational spring '.'

            # shorten start
            if len(row) > 0 and row[0] == "#":
                # remove the '##' and one '.'
                row = row[rec[0] + 1 :]
                # remove the first record, don't need it
                rec = rec[1:]
                continue

            # shorten end
            if len(row) > 0 and row[len(row) - 1] == "#":
                # remove the '##' and one '.'
                row = row[: len(row) - rec[len(rec) - 1] - 1]
                # remove the first record, don't need it
                rec = rec[: len(rec) - 1]
                continue

            # spaces equal the expected number of broken springs
            if len(row) > 0 and len(row) == rec[0]:
                row = ""
                rec = rec[1:]
                continue

            # if we have only a continuous chunk of '?'
            if len(row) > 0 and row.count("?") == len(row):
                if len(rec) == 1:
                    # we know rec < len(row) because of previous rule above
                    posib *= (len(row) - rec[0]) + 1
                    row = ""
                    rec = rec[1:]
                    continue

                if len(rec) > 1:
                    # if the ???? is full given the number of records
                    if len(row) == (len(rec) * 2 - 1):
                        row = ""
                        rec = rec[len(rec) :]
                        continue
                    else:
                        # trickier, stuff can move in the space
                        pass

            # if we have some records left
            if len(rec) > 0:

                # if we can see the largest chunk (and there aren't multiple!)
                mrec = max(rec)
                if sum(np.array(rec) == mrec) == 1:
                    try:
                        hvloc = row.index("#" * mrec)
                        # record is first or last then cut off ends
                        # left
                        if mrec == rec[0]:
                            rec = rec[1:]
                            row = row[hvloc + mrec + 1 :]
                            continue
                        # right
                        if mrec == rec[len(rec) - 1]:
                            rec = rec[0:-1]
                            row = row[: hvloc - 1]
                            continue
                        # if not left or right, then middle
                        # remove largest from records
                        rec.remove(mrec)
                        row = (
                            row[: hvloc - 1]
                            + ("." * (mrec + 2))
                            + row[hvloc + mrec + 1]
                        )
                        continue
                    except ValueError:
                        pass

            # just brute force any remaining chunks?

            # we've solved it - only one instance
            if len(row) == 0:
                if len(rec) > 0:
                    exit("Unexpected!")
                    if len(rec) > 0:
                        exit("Unexpected!")
                break

            if rlen == len(row):
                # no change
                break

        if len(rec) > 0:
            print(row, rec)
        tot_posib.append(posib)


print("#### Part 1 ####")
print("Answer is:", sum(tot_posib))


# PART 2 ####
print("============ Part 2 start ================")

print("#### Part 2 ####")
print(
    "Answer is:",
)
