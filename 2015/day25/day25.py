"""AoC 2015 - Day 25."""

# import math
# import re
# import copy
# import json
# import numpy as np
# import cmcaoc as cmc
# import functools  # for memoization


def solve(ty, tx):

    print("Solve", ty, tx)
    y = x = 1

    val = 20151125
    mult = 252533
    mod = 33554393

    while True:
        # get next position
        if y == 1:
            y = x + 1
            x = 1
        else:
            y -= 1
            x += 1

        # calculate value
        # print(y, x, val, end=" ")
        val = (val * mult) % mod
        # print(val)

        if y == ty and x == tx:
            return val


def tests():
    """Run some tests."""
    assert solve(2, 1) == 31916031
    assert solve(3, 1) == 16080970
    assert solve(4, 1) == 24592653
    assert solve(6, 6) == 27995004
    print("All tests passed!")


def part1():
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = solve(2978, 3083)
    print("Part 1 answer is:", answer)


def part2():
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    answer = 0
    print("Part 2 answer is:", answer)


if __name__ == "__main__":
    tests()
    part1()
    # part2()
