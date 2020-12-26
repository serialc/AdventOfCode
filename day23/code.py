import re
import numpy as np
import math

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

input_file = 'input_test'
input_file = 'input'

cupcircle = []
with open(input_file, 'r') as fh:
    for line in fh:
        line = line.rstrip()

        cupcircle = [int(n) for n in line]

# cupcircle is a list with position order of labelled cups

# 100 moves
moves = 100
curcuploc = 0
for m in range(1, moves+1):
    curcuplab = cupcircle[curcuploc]

    print("-- move " + str(m) + " --")
    cupsstr = "".join([" " + str(c) + " " if c != curcuplab else "("+str(c)+")" for c in cupcircle])
    print("cups: " + cupsstr)

    # remove next three after curcuploc
    popped = []
    for i in range(3):
        if (curcuploc+1) == len(cupcircle):
            popped.append(cupcircle.pop(0))
        else:
            popped.append(cupcircle.pop(curcuploc+1))
    print("pick up:", ", ".join([str(p) for p in popped]))

    # what are the min and max labels left in circle
    cmin = min(cupcircle)
    cmax = max(cupcircle)

    # need to update curcuploc!
    for i in range(len(cupcircle)):
        if cupcircle[i] == curcuplab:
            curcuploc = i

    # find label of cup we should place picked-up cups after
    destcuplab = cupcircle[curcuploc] - 1

    # find the location of the destcuplabel
    destcuploc = None
    while destcuploc == None:
        for cloc in range(len(cupcircle)):
            if cupcircle[cloc] == destcuplab:
                destcuploc = cloc
        if destcuploc == None:
            destcuplab -= 1
            if destcuplab < cmin:
                destcuplab = cmax

    # place cups
    print("destination:", destcuplab, "\n")
    for i in range(len(popped)):
        cupcircle.insert(destcuploc + 1 + i, popped[i])

    # increment for next loop
    while cupcircle[curcuploc] != curcuplab:
        cupcircle.append(cupcircle.pop(0))
    curcuploc = (curcuploc + 1)%len(cupcircle)

print(cupcircle)

start = cupcircle.index(1)
substr = ""
for i in range(1, len(cupcircle)):
    substr += str(cupcircle[(start + i)%len(cupcircle)])

print("Part 1 - substring is", substr)


