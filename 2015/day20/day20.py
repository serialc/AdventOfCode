"""AoC 2015 - Day 20."""

import math
import numpy as np

# import re
# import json
# import cmcaoc as cmc
import functools  # for memoization


# memoization
@functools.cache
def getFactorPerm(factors, fp=1, depth=0):
    """Return a list of all factor combinations provided."""
    if len(factors) == 0:
        return [fp]

    fplist = []
    fplist += getFactorPerm(factors[1:], fp * factors[0], depth + 1)
    fplist += getFactorPerm(factors[1:], fp, depth + 1)

    return fplist


def getPresNum(housenum, pph, ehv):
    """Returns the number of presents a house will get."""
    # print("====> Solve for", housenum)
    # get factors of house number
    factors = []
    i = 1
    houseval = housenum
    while i < houseval:
        i += 1
        if (houseval % i) == 0:
            factors.append(i)
            houseval = int(houseval / i)
            i = 1

    fp = getFactorPerm(tuple(factors))
    # remove duplicates
    fpc = []
    for f in fp:
        if f not in fpc:
            fpc.append(f)

    presents = 0
    for f in fpc:
        # for each factor, determine if this house still gets a present
        if ehv < np.inf and housenum > (ehv * f):
            continue
        presents += f * pph
    # print("House", housenum, "gets", presents, "presents")
    return presents


def main(limit, housenum=1, pph=10, ehv=np.inf):
    """Returns first house number with presents equal or greater than limit provided."""
    # guess the range to speed up
    hpres = 0
    hpres_max = 0
    while hpres < limit:
        housenum += 1
        hpres = getPresNum(housenum, pph, ehv)

        # track maximum number of presents for progress logging
        if hpres > hpres_max:
            hpres_max = hpres
            print("House", housenum, "received", hpres, "presents")

    print("Found housenumber", housenum)
    return housenum


def tests():
    """Run some tests."""
    assert getPresNum(2, 10, np.inf) == 30
    assert getPresNum(3, 10, np.inf) == 40
    assert getPresNum(4, 10, np.inf) == 70
    assert getPresNum(5, 10, np.inf) == 60
    assert getPresNum(6, 10, np.inf) == 120
    assert getPresNum(7, 10, np.inf) == 80
    assert getPresNum(8, 10, np.inf) == 150
    assert getPresNum(9, 10, np.inf) == 130
    assert getPresNum(53, 11, 50) == 583
    assert main(100) == 6
    print("All tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = main(data, 831000)
    print("Part 1 answer is:", answer)
    # 450007030 - too high. Lots still not working properly.
    # 1297444330 - yeah yeah, I know. I didn't read the question carefully and I'm stubborn like that.


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    answer = main(data, 880000, 11, 50)
    print("Part 2 answer is:", answer)
    # 803880 - too low.


if __name__ == "__main__":
    # data = loadInput("input0")
    tests()

    # data = loadInput("input")
    part1(36000000)
    part2(36000000)
