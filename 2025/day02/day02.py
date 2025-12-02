"""AoC 2024 - Day 1."""

input_file = "input0"
input_file = "input"

ranges = []
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        ranges = line.split(",")

invalid = []

for r in ranges:
    r1, r2 = [int(x) for x in r.split("-")]

    # go through all numbers inclusive
    for v in range(r1, r2 + 1):
        # only look at number of even length
        vlen = len(str(v))
        if vlen % 2 == 0:
            vsplit = int(vlen / 2)
            if str(v)[:vsplit] == str(v)[vsplit:]:
                invalid.append(v)


print("#### Part 1 ####")
print("Answer is:", sum(invalid))

# PART 2 ####
print("============ Part 2 start ================")


def isRepetition(val):
    """
    Determine if a number is a repetition of a pattern.

    Pattern can be of any length. E.g. 11, 123123123, 1212121212
    """
    vlen = len(str(val))
    strval = str(val)

    # look for three or more repetitions
    for reps in range(2, vlen + 1):

        # only look at those where that multiple is possible
        if vlen % reps == 0:
            digits = int(vlen / reps)
            if strval == reps * strval[0:digits]:
                return True
    return False


p2invalid = []
for r in ranges:
    r1, r2 = [int(x) for x in r.split("-")]

    # go through all values inclusive
    for v in range(r1, r2 + 1):
        if isRepetition(v):
            p2invalid.append(v)

print("#### Part 2 ####")
print("Answer is:", sum(p2invalid))
