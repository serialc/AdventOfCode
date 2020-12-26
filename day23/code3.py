#import re
import numpy as np
#import math
import time

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

fullcirclesize = 9
fullcirclesize = 1000000
cupcircle = np.array(range(1,fullcirclesize+1), dtype=int)

with open(input_file, 'r') as fh:
    for line in fh:
        line = line.rstrip()

        for i in range(len(line)):
            cupcircle[i] = int(line[i])

# cupcircle is an ordered list of labelled cups
print("Finished filling list")

# create dict, label-keyed that holds the next cup label
cupdict = {}
for i in range(len(cupcircle)):
    cupdict[cupcircle[i]] = cupcircle[(i+1)%fullcirclesize]

# number of moves
moves = 10
moves = 100
moves = 10 * fullcirclesize

curcup = cupcircle[0]

for m in range(1, moves+1):
    # progress
    if m%(fullcirclesize) == 0:
        print("-- move " + str(m) + " --")
    #print("-- move " + str(m) + " --")

    cmax = fullcirclesize
    nextcup = cupdict[curcup]

    # point curcup to three farther than now
    cupdict[curcup] = cupdict[cupdict[cupdict[cupdict[curcup]]]]

    # place the orphans in popped
    popped = [nextcup, cupdict[nextcup], cupdict[cupdict[nextcup]]]
    # what is the max left in cupcircle
    for p in sorted(popped, reverse=False):
        if p == cmax:
            cmax -= 1

    #print("Pick up", popped)

    # find label of cup we should place picked-up cups after
    destcup = curcup - 1

    # find the location of the destcup
    while destcup in popped:
        destcup -= 1
        if destcup < 1:
            destcup = cmax
    if destcup < 1:
        destcup = cmax

    #print("destination", destcup, "\n")

    cupdict[popped[2]] = cupdict[destcup]
    cupdict[destcup] = popped[0]

    # need to update curcup
    curcup = cupdict[curcup]

if fullcirclesize == 9:
    substr = ""
    nextcup = 1
    while cupdict[nextcup] != 1:
        substr += str(cupdict[nextcup])
        nextcup = cupdict[nextcup]

    print("Part 1 - string is", substr)

print("Next two cups after cup 1 are",cupdict[1], cupdict[cupdict[1]])

print("Part 2 - product is", cupdict[1] * cupdict[cupdict[1]])
