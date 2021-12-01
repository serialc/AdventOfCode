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

trans = {}
ingcount = {}
# create list of possible strings
with open(input_file, 'r') as fh:
    row = 0
    for line in fh:
        line = line.rstrip()

        line = line.rstrip(')')

        ings, allerg = line.split(" (contains ")

        lineinglist = ings.split(" ")
        lineallerlist = allerg.split(", ")

        # just count the occurance of each ingredient
        for ing in lineinglist:
            if ing in ingcount:
                ingcount[ing] += 1
            else:
                ingcount[ing] = 1

        # for each allergen, add or trim the possible ingredients
        for al in lineallerlist:

            # if it's already in the list
            # we can look for matches
            if al in trans:
                possing = []

                for ing in lineinglist:
                    if ing in trans[al]:
                        possing.append(ing)
                trans[al] = possing[:]
                        
            else:
                trans[al] = lineinglist

# we can solve but first we'll count the ingredients that don't contain any allergens
ingoccsum = 0
for ing in ingcount:
    presence = False
    for al in trans:
        if ing in trans[al]:
            presence = True
            break
    if not presence:
        ingoccsum += ingcount[ing]

#print(trans)
#print(ingcount)
print("Part 1 - Ingredients that do not contain any allergen appear",ingoccsum,"times.")

# reduce possible ingredients
while sum([len(trans[al]) for al in trans]) > len(trans):
    for al in trans:
        if len(trans[al]) == 1:
            keying = trans[al][0]
            # remove that ingredient from all other possible ingredient lists
            for als in trans:
                # don't remove yourself
                if al == als:
                    continue
                if keying in trans[als]:
                    trans[als].remove(keying)


#print(trans)

dangerlist = []
allergenkeys = list(trans.keys())
allergenkeys.sort()
for al in allergenkeys:
    dangerlist.append(trans[al][0])

print("Part 2 - Canonical dangerous ingredient list:\n" + ",".join(dangerlist))
