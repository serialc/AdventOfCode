"""AoC 2024 Day 17."""

import re

# import numpy as np
# import sys
# import functools  # for memoization
# sys.setrecursionlimit(40000)
# import time


input_file = "input0"
input_file = "input1"
input_file = "input2"
input_file = "input3"
input_file = "input"

# initialize registers
a, b, c = 0, 0, 0
prog = []  # type: list[int]

with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        res = re.match(r"Register A: (\d+)", line)
        if res:
            a = int(res.groups()[0])
            continue

        res = re.match(r"Register B: (\d+)", line)
        if res:
            b = int(res.groups()[0])
            continue

        res = re.match(r"Register C: (\d+)", line)
        if res:
            c = int(res.groups()[0])
            continue

        res = re.match(r"Program: ", line)
        if res:
            prog = [int(x) for x in line.split(" ")[1].split(",")]
            continue


print(a, b, c, prog)


# Run the program
def processProg(a, b, c, prog, brute=False):
    output = []  # type: list[int]
    pnt = 0
    while pnt < len(prog) - 1:
        op = prog[pnt]
        lop = prog[pnt + 1]
        cop = lop
        pnt += 2

        # determine the combo operand
        if lop == 4:
            cop = a
        elif lop == 5:
            cop = b
        elif lop == 6:
            cop = c

        # print( "\n=> Processing op", op, "with literal operand", lop,
        #  "and combo operand", cop,)

        if op == 0:
            # print(a, "div by 2 to power", cop)
            # a = int(a / pow(2, cop))
            # this is the same as bit shifting!
            a = a >> cop
            # print("Store in register a:", a)
        if op == 1:
            # bitwise xor of b and lop
            # print("bit XOR of", b, lop)
            b = b ^ lop
            # print("resolves to", b)
        if op == 2:
            # print(cop, "modulo 8")
            b = cop % 8
            # print("resolves to", b)
        if op == 3:
            if a != 0:
                # set the pointer to the value of the previous instruction (back one)
                pnt = lop
                # print("Set pointer to", pnt)
        if op == 4:
            # bitwise xor of b and c
            # print("bit XOR of", b, c)
            b = b ^ c
            # print("resolves to", b)
        if op == 5:
            # print("Added ", cop, "% 8 =", cop % 8, "to output")
            output.append(cop % 8)

            # check if we the output is replicating the program
            if brute:
                if prog[: len(output)] == output:
                    # print("So far so good", output)
                    pass
                else:
                    # print("Tried to append the value", cop % 8)
                    return False

        if op == 6:
            # print(a, "div by 2 to power", cop)
            b = a >> cop
            # b = int(a / pow(2, cop))
            # print("Store in register b:", b)
        if op == 7:
            # print(a, "div by 2 to power", cop)
            c = a >> cop
            # c = int(a / pow(2, cop))
            # print("Store in register c:", c)

    return output


output = processProg(a, b, c, prog)

print("#### Part 1 ####")
print("Answer is:", ",".join([str(i) for i in output]))
# 6,4,1,4,2,3,4,2,0 - nope. Was using the combo operator all the time!

# PART 2 ####
print("============ Part 2 start ================")

# We want the output to match the program input
# What register value does A need to be set to?
# We want this output
# 2,4,1,1,7,5,1,5,4,3,5,5,0,3,3,0
# Tried brute forcing - was going to take at least a few days/weeks

print(prog)

# buy let's start by trying from the start of the program
# Need a 2 printed
# (2,4) modulo A by 8 -> B: b = 0-7, a = x * 8 + b :: 1
# (1,1) bit XOR B ^ 1 -> B: b -/+ 1, b = 0-7 :: 0
# (7,5) A / (2**B) -> C: a / (2**(b +/- 1)) :: 1
# (1,5) bit XOR B ^ 5 -> B: b = 0-7
# (4,3) bit XOR B ^ C -> B: b = c +/- 7
# (5,5) modulo B by 8 -> out: B = x * 8 + 2


def solveP2():
    regA = 1308958392320
    # regA = 0
    notif = 2**25

    while True:
        # show progress every notif range
        for i in range(notif):
            # get program output
            pout = processProg(regA, 0, 0, prog, brute=True)
            if type(pout) is list:
                print("Candidate", regA, pout)
                if pout == prog:
                    print(regA, pout)
                    return regA

            # try next
            regA += 1
        print(regA)


# Being a brute won't work here
# soln = solveP2()

print("#### Part 2 ####")
print("Answer is:", soln)
# 129000000000 is too low - brute forcing won't work
# Replaced exponent operation and divisions with bit-shifting
# 1308958392320 is too low - brute forcing with added efficiency won't work either
