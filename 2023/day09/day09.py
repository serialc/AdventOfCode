import numpy as np
#import re

input_file = 'input0'
input_file = 'input'

newvals = []
with open(input_file, 'r') as fh:
    for l in fh:
        l = l.strip('\n')

        if l == '':
            continue

        vh = [np.array(list(map(int, l.split())))]

        lvls = 0
        while not all(np.diff(vh[lvls]) == 0):
            vh.append(np.diff(vh[lvls]))
            lvls += 1

        # reverse - add the same value as last non-zero
        vh[lvls] = np.append(vh[lvls], vh[lvls][0])
        while lvls > 0:
            part = vh[lvls] + vh[lvls-1]
            vh[lvls-1] = np.append(vh[lvls-1][0], part)
            lvls -= 1

        newvals.append(int(vh[lvls][-1]))

print("#### Part 1 ####")
print("Answer is:", sum(newvals))


#### PART 2 ####
print("============ Part 2 start ================")

input_file = 'input0'
input_file = 'input'

newvals = []
with open(input_file, 'r') as fh:
    for l in fh:
        l = l.strip('\n')

        if l == '':
            continue

        vh = [np.array(list(map(int, l.split())))]

        lvls = 0
        while not all(np.diff(vh[lvls]) == 0):
            vh.append(np.diff(vh[lvls]))
            lvls += 1

        # reverse - add the same value as last non-zero
        vh[lvls] = np.append(vh[lvls], vh[lvls][0])
        while lvls > 0:
            part = vh[lvls-1] - vh[lvls] 
            vh[lvls-1] = np.append(part, vh[lvls-1][-1])
            lvls -= 1

        newvals.append(int(vh[lvls][0]))
print("#### Part 2 ####")
print("Answer is:", sum(newvals))
