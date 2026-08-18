"""AoC 2015 - Day 8."""

# import re
# import numpy as np
# import cmcaoc as cmc
# import functools  # for memoization


def loadInput(input_file):
    """Return input data."""
    lines = []
    with open(input_file, "r") as fh:
        for line in fh:
            line = line.strip("\n")

            if line == "":
                continue

            if line[0] == "#":
                continue

            lines.append(line)

    return lines


def countChars2(line):
    print("Parsing line:", line, end="")

    line_length = len(line)

    # remove quotes for sanity
    line = line[1:-1]
    char_count = len(line)

    # uncount escaped quote \"
    char_count -= line.count('\\"')

    # uncount escaped escape
    char_count -= line.count("\\\\")

    # uncount hexadecimal notation
    char_count -= line.count("\\x") * 3

    # recount certain patterns
    char_count += line.count("\\\\x") * 3

    # this is getting stupid
    char_count -= line.count("\\\\\\x") * 3

    print(". Counted", char_count, "characters")
    return line_length - char_count


def countChars(line):
    """Count the characters."""
    print("Parsing line (", len(line), "): ", line, end="", sep="")

    line_length = len(line)
    state = None
    char_count = 0

    for c in list(line):

        if state is None:
            # if c is the character '\'
            if c == "\\":
                state = "escape"
                continue

            # the starting and ending double quotes
            if c == '"':
                # don't count these, unless escaped
                continue

            char_count += 1

        if state == "escape":
            # it's an escaped slash or double quote
            if c == "\\" or c == '"':
                char_count += 1
                state = None
                continue

            # it's a multi-character encoding
            if c == "x":
                char_count += 1
                state = "hexchar"
                continue

            exit("Unexpected character '", c, "' following escape", sep="")

        if state == "hexchar":
            state = "hexchar1"
            continue
        if state == "hexchar1":
            state = None
            continue

    print(". Counted", char_count, "characters")
    return line_length - char_count


def expandChars(line):

    # double quotes on each side
    flen = 2

    # cut out the end quotes for sanity
    for c in list(line):
        if c == '"':
            flen += 2
            continue
        if c == "\\":
            flen += 2
            continue
        flen += 1

    print("Expanded", line, "from length", len(line), "to", flen)
    return flen - len(line)


def tests(data):
    """Run some tests."""
    assert countChars(data[0]) == 2
    assert countChars2(data[0]) == 2
    assert countChars(data[1]) == 2
    assert countChars2(data[1]) == 2
    assert countChars(data[2]) == 3
    assert countChars2(data[2]) == 3
    assert countChars(data[3]) == 5
    assert countChars2(data[3]) == 5
    assert countChars(data[4]) == 13
    assert countChars2(data[4]) == 13
    assert countChars(data[5]) == 5
    assert countChars2(data[5]) == 5
    assert countChars(data[6]) == 13
    assert countChars2(data[6]) == 13

    assert expandChars(data[0]) == 4
    assert expandChars(data[1]) == 4
    assert expandChars(data[2]) == 6
    assert expandChars(data[3]) == 5


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")

    char_sum = 0
    for line in data:
        m1 = countChars(line)
        m2 = countChars2(line)
        if m1 != m2:
            exit("Failure at line:" + line)

        char_sum += m1

    print("Part 1 answer is:", char_sum)
    # 4977 - too high. Didn't read the instructions carefully.


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")

    char_sum = 0
    for line in data:
        char_sum += expandChars(line)

    print("Part 2 answer is:", char_sum)


if __name__ == "__main__":
    tdata = loadInput("input0")
    tests(tdata)

    data = loadInput("input")
    part1(data)
    part2(data)
