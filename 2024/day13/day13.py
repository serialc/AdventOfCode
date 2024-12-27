"""Solves Advent of Code 2024 Day 13."""

# import numpy as np
import re


# Is not used
def getFactors(num):
    """Return a list of factors for a number."""
    factors = []
    dnum = num
    n = 2
    while n <= dnum:
        if dnum % n == 0:
            factors.append(n)
            dnum = int(dnum / n)
            # try again with the same n
            # otherwise would return factors 2,4 for 8, rather than 2,2,2
            continue
        n += 1
    if dnum != 1:
        factors.append(dnum)
    return factors


def solveButtonBalance(a, b, t):
    """Return whether a success and the A and B counts."""
    # Solve both equations
    bt = int((t[1] - (t[0] * a[1]) / a[0]) / (b[1] - (b[0] * a[1]) / a[0]) + 0.5)
    at = int((t[0] - bt * b[0]) / a[0] + 0.5)
    # print("Button 'A' pressed", at, "times")
    # print("Button 'B' pressed", bt, "times")

    if at * a[0] + bt * b[0] == t[0] and at * a[1] + bt * b[1] == t[1]:
        return (at, bt)
    return False


input_file = "input0"
input_file = "input"

ac = 3
bc = 1

tokens = 0
with open(input_file, "r") as fh:

    for line in fh:
        line = line.strip("\n")

        res = re.match(r"Button A: X\+(\d+), Y\+(\d+)", line)
        if res:
            a = [int(x) for x in res.groups()]
            continue

        res = re.match(r"Button B: X\+(\d+), Y\+(\d+)", line)
        if res:
            b = [int(x) for x in res.groups()]
            continue

        res = re.match(r"Prize: X=(\d+), Y=(\d+)", line)
        if res:
            t = [int(x) for x in res.groups()]
            btns = solveButtonBalance(a, b, t)

            if btns is not False:
                tcost = btns[0] * ac + btns[1] * bc
                print(btns, tcost)
                tokens += tcost

            continue


print("#### Part 1 ####")
print("Answer is:", tokens)
# 28492 - too low: some numbers (e.g. 39.99999) rounded to 39 rather than 40


# PART 2 ####
print("============ Part 2 start ================")

tokens = 0
with open(input_file, "r") as fh:

    for line in fh:
        line = line.strip("\n")

        res = re.match(r"Button A: X\+(\d+), Y\+(\d+)", line)
        if res:
            a = [int(x) for x in res.groups()]
            continue

        res = re.match(r"Button B: X\+(\d+), Y\+(\d+)", line)
        if res:
            b = [int(x) for x in res.groups()]
            continue

        res = re.match(r"Prize: X=(\d+), Y=(\d+)", line)
        if res:
            # Part 2 change! Added 10000000000000 to target
            t = [int(x) + 10000000000000 for x in res.groups()]
            btns = solveButtonBalance(a, b, t)

            if btns is not False:
                tcost = btns[0] * ac + btns[1] * bc
                print(btns, tcost)
                tokens += tcost

            continue
print("#### Part 2 ####")
print("Answer is:", tokens)
