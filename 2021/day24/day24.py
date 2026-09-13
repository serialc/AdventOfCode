"""AoC 2021 - Day 24."""

import re

# import cmcaoc as cmc
# import numpy as np


def loadInput(input_file):
    """Retrieve data in usable form."""
    data = []
    with open(input_file, "r") as fh:
        for line in fh:
            line = line.strip("\n")

            if line == "":
                continue

            if line[0] == "#":
                continue

            p = line.split(" ")
            data.append({"cmd": p[0], "params": p[1:]})
    return data


def groupInput(data):
    """Repackages input into protocol groups."""
    protocols = []
    group = []
    for cp in data:
        cmd = cp["cmd"]
        if len(group) != 0 and cmd == "inp":
            protocols.append(group)
            group = []

        group.append(cp)
    protocols.append(group)

    return protocols


def processDigit(protocol, digit, z):
    """Process z across protocol with input w."""
    reg = {"w": 0, "x": 0, "y": 0, "z": z}
    # print("processDigit(", digit, z, ")")
    # print(protocol)

    ptype_decr = False
    if protocol[4]["params"][1] == "26":
        ptype_decr = True

    for cp in protocol:
        cmd = cp["cmd"]
        p = cp["params"]

        # print("Command", cmd, ", param.", p)

        if cmd == "inp":
            reg[p[0]] = digit

        # check if second parameter is a number
        p2n = False
        if len(p) == 2 and re.match(r"-?\d+", p[1]):
            p2n = True

        if cmd == "add":
            if p2n:
                reg[p[0]] = reg[p[0]] + int(p[1])
            else:
                reg[p[0]] = reg[p[0]] + reg[p[1]]

        if cmd == "mul":
            if p2n:
                reg[p[0]] = reg[p[0]] * int(p[1])
            else:
                reg[p[0]] = reg[p[0]] * reg[p[1]]

        if cmd == "div":
            if p2n:
                reg[p[0]] = int(reg[p[0]] / int(p[1]))
            else:
                reg[p[0]] = int(reg[p[0]] / reg[p[1]])

        if cmd == "mod":
            if p2n:
                reg[p[0]] = reg[p[0]] % int(p[1])
            else:
                reg[p[0]] = reg[p[0]] % reg[p[1]]

        if cmd == "eql":
            if p2n:
                reg[p[0]] = (reg[p[0]] == int(p[1])) * 1
            else:
                reg[p[0]] = (reg[p[0]] == reg[p[1]]) * 1

    # if of decrement type but new z is greater than passed, z, this is bad
    if ptype_decr and reg["z"] > z:
        return False

    return reg["z"]


def checkNumValid2(protocols, numstr):
    """Checks each digit and processes it for MONAD compliance."""
    indigits = [int(x) for x in list(numstr)]

    z = 0
    for i in range(len(indigits)):
        z = processDigit(protocols[i], indigits[i], z)
        print(indigits[i], "->", z)
    return z


def checkNumValid(protocol, numstr):
    """Checks each digit and processes it for MONAD compliance."""
    indigits = [int(x) for x in list(numstr)]

    # initialize all registers to 0
    reg = {"w": 0, "x": 0, "y": 0, "z": 0}

    for cp in protocol:
        cmd = cp["cmd"]
        p = cp["params"]

        # print("Command", cmd, ", param.", p)

        if cmd == "inp":
            reg[p[0]] = indigits.pop(0)

        # check if second parameter is a number
        p2n = False
        if len(p) == 2 and re.match(r"-?\d+", p[1]):
            p2n = True

        if cmd == "add":
            if p2n:
                reg[p[0]] = reg[p[0]] + int(p[1])
            else:
                reg[p[0]] = reg[p[0]] + reg[p[1]]

        if cmd == "mul":
            if p2n:
                reg[p[0]] = reg[p[0]] * int(p[1])
            else:
                reg[p[0]] = reg[p[0]] * reg[p[1]]

        if cmd == "div":
            if p2n:
                reg[p[0]] = int(reg[p[0]] / int(p[1]))
            else:
                reg[p[0]] = int(reg[p[0]] / reg[p[1]])

        if cmd == "mod":
            if p2n:
                reg[p[0]] = reg[p[0]] % int(p[1])
            else:
                reg[p[0]] = reg[p[0]] % reg[p[1]]

        if cmd == "eql":
            if p2n:
                reg[p[0]] = (reg[p[0]] == int(p[1])) * 1
            else:
                reg[p[0]] = (reg[p[0]] == reg[p[1]]) * 1

    print("Processing of", numstr, "finished. Z=", reg["z"])
    return reg["z"]


def decrNumber(number_str, from_left=False, digit=None):
    """Return the next lower number without a zero."""
    if digit is None:
        if from_left:
            digit = 0
        else:
            digit = len(number_str) - 1

    # prevent bad looping
    if from_left:
        if digit == len(number_str) - 1 and number_str[digit] == "1":
            exit("decrNumber() has reached end of possible numbers to generate.")
    else:
        if digit == 0 and number_str[digit] == "1":
            exit("decrNumber() has reached end of possible numbers to generate.")

    # loop down 1 -> 9
    if number_str[digit] == "1":
        number_str[digit] = "9"
        # depending on increment direction left/right
        if from_left:
            number_str = decrNumber(number_str, from_left, digit + 1)
        else:
            number_str = decrNumber(number_str, from_left, digit - 1)
    else:
        number_str[digit] = str(int(number_str[digit]) - 1)
    return number_str


def deepSeek(protos, z=0, digits=[], depth=0):
    """Recursively seek valid ids."""
    res_list = []
    # print("deepSeek", z, digits, depth, "\n")

    # show progress
    if depth == 6:
        print("Progress", "".join(map(str, digits)))

    # if created 14 digit id, check z value
    if depth == 14:
        if z == 0:
            vid = "".join(map(str, digits))
            print("Found", vid)
            return [int(vid)]
        return False

    # try digits 1-9
    for digit in range(9, 0, -1):

        # valid path
        # Use for highest id
        lowbound = [9, 6, 9, 1]
        highbound = [9, 6, 8, 1]
        # Use for lowest id
        lowbound = [9, 1, 8, 1]
        highbound = [9, 1, 8, 1]
        blen = len(lowbound)

        if depth >= 1 and depth <= blen:
            if (
                digits[depth - 1] > lowbound[depth - 1]
                or digits[depth - 1] < highbound[depth - 1]
            ):
                continue

        # get the z value up to this depth
        nz = processDigit(protos[depth], digit, z)
        if nz is False:
            continue

        # recurse down to next digit
        res = deepSeek(protos, nz, digits.copy() + [digit], depth + 1)

        if res is not False and len(res) != 0:
            res_list += res
    return res_list


def main(protocol, largest=True):
    """Returns the largest fourteen digit number that is MONAD valid."""
    # get the grouped protocols
    gproto = groupInput(protocol)

    res = deepSeek(gproto)
    if largest:
        return max(res)
    return min(res)


def tests(data):
    """Run some tests."""
    assert checkNumValid(data, "39") == 1
    gdata = groupInput(data)
    assert checkNumValid2(gdata, "39") == 1
    print("All tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = main(data)
    print("Part 1 answer is:", answer)


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    answer = main(data, False)
    print("Part 2 answer is:", answer)
    # 96811241911691 - too high


if __name__ == "__main__":
    # data = loadInput("input0")
    # tests(data)

    data = loadInput("input")
    # part1(data)
    part2(data)
