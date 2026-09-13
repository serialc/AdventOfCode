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
                print("eql", p[0], p[1], reg[p[0]], reg[p[1]])
                reg[p[0]] = (reg[p[0]] == reg[p[1]]) * 1
    return reg["z"]


def checkNumValid2(protocols, numstr):
    """Checks each digit and processes it for MONAD compliance."""
    indigits = [int(x) for x in list(numstr)]

    z = 0
    for i in range(len(indigits)):
        z = processDigit(protocols[i], indigits[i], z)
        print(indigits[i], "->", z)
    return z


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
    if depth == 6:
        print("".join(map(str, digits)), z)
        if z == 1:
            return "".join(map(str, digits))
        return False

    res_list = []
    for digit in range(1, 10):
        res = deepSeek(
            protos, processDigit(protos[depth], digit, z), digits + [digit], depth + 1
        )

        if res is not False:
            res_list += res

    return res_list


def condenseInstructions(protos):
    """Condense the instructions and display them."""
    special = [4, 5, 15]
    for i in range(len(protos[0])):
        cmd = protos[0][i]["cmd"]
        params = protos[0][i]["params"]

        if i in special:
            print("Instruction", i, cmd, params[0], end="= ")

            for p in protos:
                print(p[i]["params"][1], end=" ")
            print()
        else:
            print("Instruction", i, cmd, params)


def main(protocol):
    """Returns the largest fourteen digit number that is MONAD valid."""
    # get the grouped protocols
    gproto = groupInput(protocol)
    condenseInstructions(gproto)

    # the values on line following the div/1 (when present) is not relevent,
    # always resolves to the multiplication of z by 26

    z3 = 38
    z4 = processDigit(gproto[4], 8, z3)
    z5 = processDigit(gproto[4], 9, z4)
    print(z3, z4, z5)
    return checkNumValid2(gproto, "999999999999")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = main(data)
    print("Part 1 answer is:", answer)


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    answer = main(data)
    print("Part 2 answer is:", answer)


if __name__ == "__main__":
    # data = loadInput("input0")
    # tests(data)

    data = loadInput("input")
    part1(data)
    # part2(data)
