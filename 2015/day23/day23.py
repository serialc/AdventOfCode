"""AoC 2015 - Day 23."""

import re

# import math
# import numpy as np
# import copy
# import json
# import cmcaoc as cmc
# import functools  # for memoization


def loadInput(input_file):
    """Return input data."""
    data = []
    with open(input_file, "r") as fh:
        for line in fh:
            line = line.strip("\n")

            if line == "":
                continue

            ins = re.match(r"(\w+) (.+)$", line)
            cmd, par = ins.groups()
            data.append([cmd, par])
    return data


def turing(data, p2=False):

    reg = {"a": 0, "b": 0}
    if p2:
        reg = {"a": 1, "b": 0}

    i = 0

    while True:
        if i >= len(data):
            break
        cmd, par = data[i]

        if cmd == "hlf":
            reg[par] = int(reg[par] / 2)
        if cmd == "tpl":
            reg[par] = int(reg[par] * 3)
        if cmd == "inc":
            reg[par] += 1
        if cmd == "jmp":
            i += int(par)
            continue
        if cmd == "jie":
            par, offset = par.split(", ")
            if reg[par] % 2 == 0:
                i += int(offset)
                continue
        if cmd == "jio":
            par, offset = par.split(", ")
            if reg[par] == 1:
                i += int(offset)
                continue

        # go to next instruction
        i += 1
    return reg


def tests(data):
    """Run some tests."""
    assert turing(data)["a"] == 2
    print("All tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = turing(data)["b"]
    print("Part 1 answer is:", answer)


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    answer = turing(data, True)["b"]
    print("Part 2 answer is:", answer)


if __name__ == "__main__":
    data = loadInput("input0")
    tests(data)

    data = loadInput("input")
    part1(data)
    part2(data)
