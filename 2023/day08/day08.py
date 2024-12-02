#from math import prod
#import numpy as np
#import re

input_file = 'input0'
input_file = 'input'

def genParts(input_file):
    inst = None
    paths = dict()
    with open(input_file, 'r') as fh:
        for l in fh:
            l = l.strip('\n')

            if l == '':
                continue

            if inst is None:
                inst = list(l)
                continue

            name, sp = l.split(' = ')
            # sp = '(BBB, CCC)'
            paths[name] = sp[1:-1].split(', ')
    return inst, paths

# get puzzle
inst, paths = genParts(input_file)

loc = 'AAA'
i = 0
count = 0
while loc != 'ZZZ':
    #print(loc)
    if inst[i] == 'L':
        loc = paths[loc][0]
    else:
        loc = paths[loc][1]

    # increment and reset if necessary
    i = (i + 1)%len(inst)
    count += 1
#print(loc)
        
print("#### Part 1 ####")
print("Answer is:", count)

#### PART 2 ####
print("============ Part 2 start ================")

input_file = 'input1'
input_file = 'input'

# get puzzle
inst, paths = genParts(input_file)

# get the starts of the form '--A'
locs = [code for code in paths if code[2] == 'A']

# ok, takes forever, need to run individually and then determine
# lowest common multiple of all the path counts for a match

pathcounts = []
for loci in range(len(locs)):
    insti = 0
    count = 0
    while True:
        if inst[insti] == 'L':
            locs[loci] = paths[locs[loci]][0]
        else:
            locs[loci] = paths[locs[loci]][1]

        # increment and reset if necessary
        insti = (insti + 1)%len(inst)
        count += 1

        # check if all are pointing at an '--X'
        if locs[loci][2] == 'Z':
            pathcounts.append(count)
            break

print('path counts', pathcounts)

# ok, now we need to find the least common multiple
# get the factors for each one
factors = []
for i in range(len(pathcounts)):
    pc = pathcounts[i]
    n = 2
    pcf = []
    while n <= pc:
        if pc%n == 0:
            pcf.append(n)
            pc = int(pc/n)
        n += 1
    factors.append(pcf)

print('factors', factors)

# now get the unique factors
lcm_factors = []
lcm = 1
for f in factors:
    for i in f:
        if i not in lcm_factors:
            lcm_factors.append(i)
            lcm *= i

print('lcm_factors', lcm_factors)

print("#### Part 2 ####")
print("Answer is:", lcm)
