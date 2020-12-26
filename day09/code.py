import numpy as np
import re

size = 5
size = 25
filename = 'input_test.txt'
filename = 'input.txt'

# build data in dict
stack = []
with open(filename,'r') as fh:
    lnum = 0
    for line in fh:
        val = int(line.rstrip())

        if len(stack) < size:
            stack.append(val)
            continue

        works = False
        for i in range(size):
            # check for each value in stack
            # - value minus stack item is in stack
            # - make sure the match isn't half of val
            if val - stack[i] in stack and stack[i]*2 != val:
                works = True

        if not works:
            break

        # adjust stack
        stack.pop(0)
        stack.append(val)

print("\nPart 1: " + str(val))


# Part 2
target = val

# build data in dict
stack = []
with open(filename,'r') as fh:
    lnum = 0
    for line in fh:
        val = int(line.rstrip())

        stack.append(val)

        #print(val, sum(stack), stack)
        # if ssum < target: # do nothing - add more to stack
        while sum(stack) > target:
            # pop first element from stack
            stack.pop(0)
        if sum(stack) == target:
            print("Found it!")
            break

print(stack)
print("\nPart 2: " + str(min(stack) + max(stack)))
