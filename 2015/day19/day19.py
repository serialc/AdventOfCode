"""AoC 2015 - Day 19."""

import re

# import json
# import numpy as np
# import cmcaoc as cmc
# import functools  # for memoization


def loadInput(input_file):
    """Return input data."""
    data = {}
    starter = ""
    with open(input_file, "r") as fh:
        for line in fh:
            line = line.strip("\n")

            if line == "":
                continue

            sm = re.match(r"(\w+) => (\w+)", line)
            if sm:
                mfrom, mto = sm.groups()
                if mfrom in data:
                    data[mfrom].append(mto)
                else:
                    data[mfrom] = [mto]
            else:
                starter = line
    return {"start": starter, "dict": data}


def createMolecules(data):
    """Return number of unique molecules that can be created."""
    start = data["start"]
    mcd = data["dict"]

    mols = []
    for i in range(len(start)):
        # look at next one or two characters and see if they fit in dict
        # two character keys
        if i < (len(start) - 1):
            mchar = start[i : i + 2]
            if mchar in mcd:
                for mpat in mcd[mchar]:
                    newmol = start[:i] + mpat + start[i + 2 :]
                    if newmol not in mols:
                        mols.append(newmol)
        # one character keys
        if start[i] in mcd:
            for mpat in mcd[start[i]]:
                newmol = start[:i] + mpat + start[i + 1 :]
                if newmol not in mols:
                    mols.append(newmol)
    return len(mols)


def reverseMolecule(md, data, count=0):
    """Recursively shorten molecule until it is 'e' and return recursion count."""
    if data == "e":
        return count

    # Note: This only works because the provided string isn't evil.
    # --> Keys don't contain other keys.
    # Don't need to search entire space

    # for each pattern
    for k, v in md.items():
        # if it is inside string
        if data.count(k) > 0:
            # replace first instance with the shorter string
            ki = data.index(k)
            return reverseMolecule(md, data[:ki] + v + data[ki + len(k) :], count + 1)


def reverseDictList(data):
    """Takes dict containing lists, reverses it, and saves as a global."""
    md = {}
    # reverse the molecule dict
    for k, vlist in data.items():
        for v in vlist:
            md[v] = k
    return md


def tests(data):
    """Run some tests."""
    assert createMolecules(data) == 4
    print("All tests passed!")


def tests2(data):
    """Run some more tests."""
    md = reverseDictList(data["dict"])
    assert reverseMolecule(md, "HOH") == 3
    assert reverseMolecule(md, "HOHOHO") == 6
    print("All additional tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = createMolecules(data)
    print("Part 1 answer is:", answer)


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    md = reverseDictList(data["dict"])
    answer = reverseMolecule(md, data["start"])
    print("Part 2 answer is:", answer)


if __name__ == "__main__":
    data = loadInput("input0")
    tests(data)
    data = loadInput("input1")
    tests2(data)

    data = loadInput("input")
    part1(data.copy())
    part2(data.copy())
