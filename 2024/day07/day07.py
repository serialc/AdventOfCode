import numpy as np
# import re

input_file = 'input0'
input_file = 'input'


def EquSolve(val, comp, ops=[], p2=False):

    if len(ops) == (len(comp) - 1):
        for op in ops:
            # reduce multiplications
            if op == '*':
                # careful
                comp[0] = comp[0] * comp.pop(1)

            # reduce sums
            if op == '+':
                comp[0] = comp[0] + comp.pop(1)

            # concatenate
            if op == '||':
                comp[0] = int(str(comp[0]) + str(comp.pop(1)))

        if comp[0] == val:
            return True

        return False

    # pass copies, otherwise you're modifying the same object
    if EquSolve(val, comp.copy(), ops.copy() + ['+'], p2):
        return True
    if EquSolve(val, comp.copy(), ops.copy() + ['*'], p2):
        return True
    if p2:
        if EquSolve(val, comp.copy(), ops.copy() + ['||'], p2):
            return True

    return False


truesum = 0
with open(input_file, 'r') as fh:
    for line in fh:
        line = line.strip('\n')

        if line == '':
            continue

        val, eqn = line.split(': ')
        val = int(val)
        comp = list(map(int, eqn.split(' ')))

        # reverse list to make debug easier
        if EquSolve(val, comp.copy()):
            # I'm dumb
            # truesum += 1
            truesum += val


print("#### Part 1 ####")
print("Answer is:", truesum)
# 287 is too low - was adding correct equations, not the sum


# PART 2 ####
print("============ Part 2 start ================")

truesum = 0
with open(input_file, 'r') as fh:
    for line in fh:
        line = line.strip('\n')

        if line == '':
            continue

        val, eqn = line.split(': ')
        val = int(val)
        comp = list(map(int, eqn.split(' ')))

        # reverse list to make debug easier
        if EquSolve(val, comp.copy(), p2=True):
            truesum += val

print("#### Part 2 ####")
print("Answer is:", truesum)
# 5030892084481 is too low - idiot again, copied the result from part one!
