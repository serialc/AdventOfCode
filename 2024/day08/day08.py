"""Solves Advent of Code Day08."""

import numpy as np
# import re


def matPrint(mat, sep=''):
    """
    Print a matrix nicely.

    Takes a numpy 2d array and prints values in a variable
    dense manner.
    """
    nh, nw = mat.shape
    print("Dimension", nh, nw)

    for y in range(nh):
        for x in range(nw):
            print(str(mat[y, x]) + sep, end='')
        print()


# build a frequency dictionary
def makeFreqDict(mat):
    """
    Get item frequency.

    Takes a numpy array and returns a dict with
    items as keys and the frequency as the value
    """
    fd = dict()
    for row in mat:
        for item in row:
            if item in fd:
                fd[item] += 1
            else:
                fd[item] = 1
    return fd


input_file = 'input0'
input_file = 'input'


lsurf = []
with open(input_file, 'r') as fh:
    for line in fh:
        line = line.strip('\n')

        if line == '':
            continue

        lsurf.append(list(line))

surf = np.array(lsurf)
matPrint(surf)


# get the list of antennas
afreq = makeFreqDict(surf)
# don't want '.' item
del afreq['.']

# save our solutions here
antinodes = np.zeros(surf.shape, dtype=int)

# for each antenna class
for ant in afreq:

    # print('Processing', ant)

    if afreq[ant] == 1:
        print("Skipping as this antenna class only has one member")
        continue

    antlocs = np.where(surf == ant)
    # antlocs is a list of two lists ((y,...), (x,...))

    # matPrint((surf == ant) * 1)

    # for each antenna
    for i in range(len(antlocs[0])):
        ay = antlocs[0][i]
        ax = antlocs[1][i]

        # get the distances to each other antenna of the same class
        for j in range(i + 1, len(antlocs[0])):
            a2y = antlocs[0][j]
            a2x = antlocs[1][j]

            # calculate the inter-antenna manhattan distance difference
            dy = a2y - ay
            dx = a2x - ax

            # try to add a antinode at the opposing sides
            if ((ay - dy) >= 0 and (ay - dy) < surf.shape[0] and
                    (ax - dx) >= 0 and (ax - dx) < surf.shape[1]):
                antinodes[(ay - dy), (ax - dx)] += 1

            if ((a2y + dy) >= 0 and (a2y + dy) < surf.shape[0] and
                    (a2x + dx) >= 0 and (a2x + dx) < surf.shape[1]):
                antinodes[(a2y + dy), (a2x + dx)] += 1

matPrint(antinodes)

print("#### Part 1 ####")
print("Answer is:", np.sum(antinodes > 0))
# 411 too high - was not considering bounding for second antenna correctly


# PART 2 ####
print("============ Part 2 start ================")

# save our solutions here
antinodes = np.zeros(surf.shape, dtype=int)

# for each antenna class
for ant in afreq:

    # print('Processing', ant)

    if afreq[ant] == 1:
        print("Skipping as this antenna class only has one member")
        continue

    antlocs = np.where(surf == ant)
    # antlocs is a list of two lists ((y,...), (x,...))

    # matPrint((surf == ant) * 1)

    # for each antenna
    for i in range(len(antlocs[0])):
        ay = antlocs[0][i]
        ax = antlocs[1][i]

        # p2 - add antinode at location of each antenna
        antinodes[ay, ax] += 1

        # get the distances to each other antenna of the same class
        for j in range(i + 1, len(antlocs[0])):
            a2y = antlocs[0][j]
            a2x = antlocs[1][j]

            # p2 - add antinode at location of each antenna
            antinodes[a2y, a2x] += 1
            # this will overinflate, counted multiple times, no longer reliable

            # calculate the inter-antenna manhattan distance difference
            py = a2y - ay
            px = a2x - ax

            # repeat the antinodes at regular lengths
            dist = 1
            while True:
                anyf = False
                dy = py * dist
                dx = px * dist

                # try to add an antinode at the opposing sides
                if ((ay - dy) >= 0 and (ay - dy) < surf.shape[0] and
                        (ax - dx) >= 0 and (ax - dx) < surf.shape[1]):
                    anyf = True
                    antinodes[(ay - dy), (ax - dx)] += 1

                if ((a2y + dy) >= 0 and (a2y + dy) < surf.shape[0] and
                        (a2x + dx) >= 0 and (a2x + dx) < surf.shape[1]):
                    anyf = True
                    antinodes[(a2y + dy), (a2x + dx)] += 1

                if not anyf:
                    break

                dist += 1

matPrint(antinodes)

print("#### Part 2 ####")
print("Answer is:", np.sum(antinodes > 0))
# 1113 too low - didn't understand that an antinode also happens at
# each antenna that is part of same frequency
