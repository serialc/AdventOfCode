import numpy as np
import re

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

filename = 'input_test.txt'
filename = 'input_test2.txt'
filename = 'input.txt'

# build data in dict
adapt = []
with open(filename,'r') as fh:
    lnum = 0
    for line in fh:
        val = int(line.rstrip())
        adapt.append(val)

adapt.sort()
# plug voltage
adapt.insert(0,0)
# device voltage (+3 than max adapter)
adapt.append(adapt[len(adapt) - 1] + 3)

diff = []
table = {}
for i in range(len(adapt) - 1):
    val = adapt[i+1] - adapt[i]
    diff.append(val)
    if val in table:
        table[val] += 1
    else:
        table[val] = 1

#print(adapt)
#print(diff)
#print(table)

optional = 0
sections = []
secopen = None
insection = False
for i in range(len(adapt)):
    if i == 0 or i == (len(adapt) - 1):
        print(str(adapt[i]) + ' ', end='')
    elif diff[i-1] == 3:
        # is 3 more than the last - required
        print(bcolors.OKBLUE + str(adapt[i]) + bcolors.ENDC + ' ', end='')
    elif diff[i] == 3:
        # the next one is three more - required
        print(bcolors.OKCYAN + str(adapt[i]) + bcolors.ENDC + ' ', end='')
        if secopen is not None:
            sections.append([secopen, adapt[i]])
            secopen = None
        insection = False
    else:
        print(bcolors.OKGREEN + str(adapt[i]) + bcolors.ENDC + ' ', end='')
        if not insection:
            secopen = adapt[i-1]
            insection = True
        optional += 1

# Part 1 - using all adapters
print("\nPart 1 answer: " + str(table[1] * table[3]) + "\n\n")


# split into smaller sections
#print(sections)
possibilities = 1
#print(sections)
for secop, seclo in sections:
    #print(secop, seclo)
    values = [val for val in adapt if val > secop and val < seclo]
    #print(values)

    combinations = 0
    for i in range(pow(2,len(values))):
        binlist = (('{0:0' + str(len(values)) + 'b}').format(i))
        # retrieve the subset of values for this test run
        testvals = [v for (v, b) in zip(values, binlist) if b == '1']

        testset = [secop] + testvals + [seclo]
        #print("Test values for this test: " + str(testvals))

        # check if any jumps are greater than 3, otherwise inc combinations
        passed = True
        for i in range(len(testset)- 1):
            if testset[i+1] - testset[i] > 3:
                passed = False
        if passed:
            combinations += 1

    #print("Combinations for set:")
    #print(values)
    #print("between " + str(secop) + " and " + str(seclo) + " are: " + str(combinations))
    if combinations > 0:
        possibilities *= combinations

# Part 2 - calculate all possible ways, using selective adapters
print("\nPart 2 answer: " + str(possibilities))
