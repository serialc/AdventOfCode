"""AoC 2015 - Day 7."""

import re

import numpy as np
import cmcaoc as cmc
import functools  # for memoization


def loadInput(input_file):
    """Return input data."""
    dd = {}
    with open(input_file, "r") as fh:
        for line in fh:
            line = line.strip("\n")

            if line == "":
                continue

            if line[0] == "#":
                continue

            ins = re.match(r"^(.+) -> ([a-z]+)$", line)
            inputs, wire = ins.groups()

            # Get simple values
            vmatch = re.match(r"^\d+$", inputs)
            if vmatch:
                dd[wire] = {"op": "VALUE", "value": np.uint16(inputs)}
                continue

            # Direct wire forwarding
            wmatch = re.match(r"^([a-z]+)$", inputs)
            if wmatch:
                dd[wire] = {"op": "WIRE", "wire": wmatch.groups()[0]}
                continue

            # Get the NOT input
            nmatch = re.match(r"^NOT ([a-z]+)$", inputs)
            if nmatch:
                dd[wire] = {"op": "NOT", "wire": nmatch.groups()[0]}
                continue

            # Get other inputs
            bo = re.match(r"^(\w+) (AND|OR|LSHIFT|RSHIFT) (\w+)$", inputs)
            if bo:
                # extract from groups
                w1, op, w2 = bo.groups()

                # inputs may be values, not just wires
                if re.match(r"\d+", w1):
                    w1 = np.uint16(w1)
                if re.match(r"\d+", w2):
                    w2 = np.int16(w2)

                dd[wire] = {"op": op, "wire1": w1, "wire2": w2}
                continue

            exit("Failed to parse line: " + line)
    return dd


# memoization
@functools.cache
def solveWire(wire, inputset):
    """Return the value associated with a wire recursively."""
    # Due to memoization we need to differentiate between calls!
    # Note the argument "inputset"
    # - Otherwise we'll get incorrect returns.

    src = data[wire]

    if src["op"] == "VALUE":
        return src["value"]

    if src["op"] == "WIRE":
        return solveWire(src["wire"], inputset)

    if src["op"] == "NOT":
        # always uses a wire, not a value, get the value
        val = solveWire(src["wire"], inputset)
        # Apply bitwise complement operation and return
        return ~val

    if src["op"] in ["AND", "OR", "LSHIFT", "RSHIFT"]:

        # Wires may contain values
        v1 = src["wire1"]
        if type(src["wire1"]) is str:
            v1 = solveWire(src["wire1"], inputset)

        v2 = src["wire2"]
        if type(src["wire2"]) is str:
            v2 = solveWire(src["wire2"], inputset)

        if src["op"] == "AND":
            return v1 & v2

        if src["op"] == "OR":
            return v1 | v2

        if src["op"] == "LSHIFT":
            return v1 << v2

        if src["op"] == "RSHIFT":
            return v1 >> v2


def tests():
    """Run some tests."""
    assert solveWire("d", "test") == 72
    assert solveWire("e", "test") == 507
    assert solveWire("f", "test") == 492
    assert solveWire("g", "test") == 114
    assert solveWire("h", "test") == 65412
    assert solveWire("i", "test") == 65079
    assert solveWire("x", "test") == 123
    assert solveWire("y", "test") == 456


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")

    print("Part 1 answer is:", solveWire("a", "p1"))
    # 33605 - Too low. Ugh, solved for "x", not "a"


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")

    # "override wire 'b' to the p1 signal you got on wire 'a'
    data["b"]["value"] = solveWire("a", "p1")

    print("Part 2 answer is:", solveWire("a", "p2"))


if __name__ == "__main__":
    data = loadInput("input0")
    tests()

    data = loadInput("input")
    part1(data)
    part2(data)
