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
#input_file = 'input'

million = 1000000
cupcircle = [0]*million
with open(input_file, 'r') as fh:
    for line in fh:
        line = line.rstrip()

        for i in range(len(line)):
            cupcircle[i] = int(line[i])

cmax = max(cupcircle)
for i in range(len(line), million):
    cmax += 1
    cupcircle[i] = cmax

# cupcircle is a list with position order of labelled cups

# number of moves
moves = 10 * million
curcuploc = 0
for m in range(1, moves+1):
    curcuplab = cupcircle[curcuploc]

    if m%(million/10) == 0:
        print("-- move " + str(m) + " --")

    # remove next three after curcuploc
    popped = []
    for i in range(3):
        if (curcuploc+1) == len(cupcircle):
            popped.append(cupcircle.pop(0))
        else:
            popped.append(cupcircle.pop(curcuploc+1))

    # what are the min and max labels left in circle
    cmin = min(cupcircle)
    cmax = max(cupcircle)

    # need to update curcuploc!
    curcuploc = cupcircle.index(curcuplab)

    # find label of cup we should place picked-up cups after
    destcuplab = cupcircle[curcuploc] - 1

    # find the location of the destcuplabel
    destcuploc = None
    while destcuploc == None:
        try:
            destcuploc = cupcircle.index(destcuplab)
        except ValueError:
            destcuplab -= 1
            if destcuplab < cmin:
                destcuplab = cmax

    # place cups
    for i in range(len(popped)):
        cupcircle.insert(destcuploc + 1 + i, popped[i])

    # need to update curcuploc!
    curcuploc = cupcircle.index(curcuplab)

    # increment for next loop
    curcuploc = (curcuploc + 1)%len(cupcircle)

oneloc = cupcircle.index(1)
print(cupcircle[oneloc:oneloc+2])

print("Part 2 - product is", cupcircle[oneloc+1] * cupcircle[oneloc+2])
