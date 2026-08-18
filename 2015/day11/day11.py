"""AoC 2015 - Day 11."""

# import re
# import numpy as np
# import cmcaoc as cmc
# import functools  # for memoization

abc = list("abcdefghijklmnopqrstuvwxyz")


def loadInput(input_file):
    """Return input data."""
    with open(input_file, "r") as fh:
        for line in fh:
            line = line.strip("\n")

            if line == "":
                continue

            if line[0] == "#":
                continue

            return line


def increment(pw):
    """Retrieve the next incremented and valid password."""
    # cursor position

    npw = list(pw)
    while True:

        cpos = len(npw) - 1

        # increment letter, and handle incrementing any carry
        while True:
            # get the next letter position/number [0-25]
            lpos = abc.index(npw[cpos]) + 1

            # help speed things up, skip 'bad' letters ("i", "l", "o")
            if lpos in [8, 11, 14]:
                lpos += 1

            # if we cycle over, "z" -> "a"
            if lpos == 26:
                npw[cpos] = "a"
                # increment the next letter to the left
                cpos -= 1

                if cpos < 0:
                    exit("Error: Cycled beyond string limit.")
            else:
                # simple letter increment
                npw[cpos] = abc[lpos]
                break

        # check validity
        if validate("".join(npw)):
            return "".join(npw)

        # not valid, try next


def validate(pw):
    """Perform validation checks on input string."""
    # includes one sequential triad
    seq_found = False
    for i in range(len(pw) - 2):

        # first letter can't be "y" or "z"
        if pw[i] in ["y", "z"]:
            continue

        # get position of this letter
        pos = abc.index(pw[i])
        if pw[i + 1] == abc[pos + 1] and pw[i + 2] == abc[pos + 2]:
            seq_found = True
            break

    if not seq_found:
        return False

    # can't contain: i o l
    if pw.count("i") > 0 or pw.count("o") > 0 or pw.count("l") > 0:
        return False

    # must contain at least two, different and distinct pairs
    pairs_found = False
    pairs = []
    for i in range(len(pw) - 1):
        # handles triplets by check if already found
        if pw[i] == pw[i + 1] and pw[i] not in pairs:
            if len(pairs) == 0:
                pairs.append(pw[i])
            else:
                pairs_found = True
                break

    if not pairs_found:
        return False

    return True


def tests():
    """Run some tests."""
    assert validate("hijklmmn") == False
    assert validate("abbceffg") == False
    assert validate("abbcegjk") == False

    assert increment("abcdefgh") == "abcdffaa"
    assert increment("ghijklmn") == "ghjaabcc"

    print("All tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")

    new_passwd = increment(data)
    print("Part 1 answer is:", new_passwd)
    return new_passwd


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")

    print("Part 2 answer is:", increment(data))


if __name__ == "__main__":
    # tdata = loadInput("input0")
    tests()

    data = loadInput("input")
    next_pass = part1(data)
    part2(next_pass)
