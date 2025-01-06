"""AoC 2024 Day 21."""

import numpy as np
import sys
import functools  # for memoization

sys.setrecursionlimit(40000)

# import time
# import re


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def keypadRequest(keystr):
    """Keypad instructions."""
    kp = np.array([["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]])

    keys_command = ""
    keys = list(keystr)
    curr = "A"
    alt = True
    for k in keys:
        keycom = ""

        # get the location of current key
        ck = np.where(kp == curr)
        ck = [ck[0][0], ck[1][0]]
        # get target key location
        tk = np.where(kp == k)
        tk = [tk[0][0], tk[1][0]]

        # print("Move from", ck, "to", tk)

        vshift = ck[0] - tk[0]
        hshift = ck[1] - tk[1]

        # need to make sure we never move over the blank button
        # otherwise robot panics - can only happen in following situations
        # - at bottom row going to left row
        # - going to bottom row from left row
        if curr in ["0", "A"] and k in ["7", "4", "1"]:
            # do ups first
            if vshift > 0:
                keycom += vshift * "^"
            if hshift > 0:
                keycom += hshift * "<"
            if vshift < 0:
                keycom += abs(vshift) * "v"
            if hshift < 0:
                keycom += abs(hshift) * ">"
        elif curr in ["7", "4", "1"] and k in ["0", "A"]:
            # do rights first
            if hshift < 0:
                keycom += abs(hshift) * ">"
            if hshift > 0:
                keycom += hshift * "<"
            if vshift < 0:
                keycom += abs(vshift) * "v"
            if vshift > 0:
                keycom += vshift * "^"
        else:
            if hshift > 0:
                keycom += hshift * "<"
            if vshift < 0:
                keycom += abs(vshift) * "v"
            if hshift < 0:
                keycom += abs(hshift) * ">"
            if vshift > 0:
                keycom += vshift * "^"

        keycom += "A"
        keys_command += keycom

        if alt:
            # print(bcolors.OKBLUE + keycom + bcolors.ENDC, end="")
            alt = False
        else:
            # print(bcolors.OKGREEN + keycom + bcolors.ENDC, end="")
            alt = True

        curr = k

    return keys_command


# memoization!
@functools.cache
def remoteRequest(key, depth, dtarget, curr="A"):
    """Control robot."""
    cp = np.array([["", "^", "A"], ["<", "v", ">"]])

    # get the location of current key
    ck = np.where(cp == curr)
    ck = [ck[0][0], ck[1][0]]
    # get target key location
    tk = np.where(cp == key[0])
    tk = [tk[0][0], tk[1][0]]

    # shift amount in V and H
    vshift = ck[0] - tk[0]
    hshift = ck[1] - tk[1]

    keycom = []
    # need to make sure we never move over the blank button
    # otherwise robot panics - can only happen in following situations
    # - at top row going to left row
    # - going to top row from left row (default handles this)
    if curr in ["^", "A"] and key[0] in ["<"]:
        if vshift < 0:
            keycom.append(abs(vshift) * "v")
        if hshift > 0:
            keycom.append(hshift * "<")
    else:
        # order matters - farthest from 'A' first
        if hshift > 0:
            keycom.append(hshift * "<")
        if vshift < 0:
            keycom.append(abs(vshift) * "v")
        # need the > before the ^ so if we're at <, we don't go over the blank
        if hshift < 0:
            keycom.append(abs(hshift) * ">")
        if vshift > 0:
            keycom.append(vshift * "^")

    keycom.append("A")

    # we will sometimes be passed doubles (e.g. "<<") rather
    # than just one key
    # If that's the case, we need to add another "A"
    if len(key) == 2:
        keycom.append("A")

    # print(depth, keycom)

    # increment our depth
    depth += 1
    if depth == dtarget:
        return len("".join(keycom))

    instr_len = 0
    curr = "A"
    for k in keycom:
        instr_len += remoteRequest(k, depth, dtarget, curr)
        curr = k[0]

    return instr_len


input_file = "input"
input_file = "input0"

complexities = []  # type: list[int]
direction_bots = 2
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        print(line, end=" ")
        # determine keypad instructions
        kpi = keypadRequest(line)
        print(kpi, end=" ")

        inst_count = 0
        currk = "A"
        for k in list(kpi):
            # print("Instruction", k)
            inst_count += remoteRequest(k, depth=0, dtarget=direction_bots, curr=currk)
            currk = k

        print(inst_count)
        complexities.append(inst_count * int(line[:-1]))

print("#### Part 1 ####")
print("Answer is:", sum(complexities))


# PART 2 ####
print("============ Part 2 start ================")

complexities.clear()

# we have one bot on the keypad
direction_bots = 24
direction_bots = 4
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        print(line, end=" ")

        # determine keypad instructions
        kpi = keypadRequest(line)

        inst_count = 0
        currk = "A"
        for k in list(kpi):
            # print("Instruction", k)
            inst_count += remoteRequest(k, depth=0, dtarget=direction_bots, curr=currk)
            currk = k

        print(inst_count)
        complexities.append(inst_count * int(line[:-1]))

print("#### Part 2 ####")
# 029A
# 2: 68
# 3: 164
# 4: 404
# 5: 998
# 6: 2482
# 7: 6166
# 10: 94910
# 15: 9041286
# 20: 861298954
print("Answer is:", sum(complexities))
print("input0 should equal to 154115708116294")
# 214633893742472 - too high: Did I do too many recursions?
# 85744151484734 - too low: No.
