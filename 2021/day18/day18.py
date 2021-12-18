import numpy as np
#import time
#from PIL import Image
import sys

#print("Recursion limit", sys.getrecursionlimit())

inputf = 'test_input'
#inputf = 'input'

def str2nested(instr):
    #print("Trying to parse", instr)

    # peel and recurse
    # first part
    divi = 0
    if instr[1].isdigit():
        lcomp = int(instr[1])
        divi = 2
    else:
        bstack = 1
        s = 2
        while bstack > 0:
            if instr[s] == '[':
                bstack += 1
            if instr[s] == ']':
                bstack -= 1
            s += 1
            
        divi = s
        lcomp = str2nested(instr[1:s])

    # second part
    if instr[-2].isdigit():
        rcomp = int(instr[-2])
    else:
        rcomp = str2nested(instr[divi + 1:-1])

    return [lcomp, rcomp]

#xp_vals = {'left': [], 'right': []}
def sfReduce(sfl, lvl=1, call_from=0, actioned=False):
    global xp_vals

    print(sfl, lvl, call_from)
    if lvl == 5 and actioned == False:
        # explode
        actioned = True
        #xp_vals['left'].append(sfl[0])
        #xp_vals['right'].append(sfl[1])
        if call_from == 0:
            return [True, sfl[1], actioned, sfl[0], sfl[1]]
        if call_from == 1:
            return [True, sfl[0], actioned, sfl[0], sfl[1]]
    else:
        # Left
        if isinstance(sfl[0], list):
            ret = sfReduce(sfl[0], lvl+1, 0, actioned)
            actioned = ret[2]
            pleft = ret[3]
            pright = ret[4]
            print("The Left returned", ret)

            # call exploded
            if ret[0]:
                return [False, [0, sfl[1] + pright], actioned, pleft, '']

            # check if we have values on the explode stack
            if pright != '' and isinstance(sfl[1], int):
                return [False, [ret[1], sfl[1] + pright], actioned, pleft, '']
            else:
                return [False, [ret[1], sfl[1]],     actioned, pleft, pright]
        # Right
        if isinstance(sfl[1], list):

            ret = sfReduce(sfl[1], lvl+1, 1, actioned)
            actioned = ret[2]
            pleft = ret[3]
            pright = ret[4]
            print("The Right returned", ret)

            # call exploded
            if ret[0]:
                return [False, [sfl[0] + pleft, 0], actioned, '', pright]

            # check if we have values on the explode stack
            if pleft != '' and isinstance(sfl[1], int):
                return [False, [sfl[0] + pleft, ret[1]], actioned, '', pright]
            else:
                return [False, [sfl[0], ret[1]],     actioned, pleft, pright]

### Read input data
sfn = []
with open(inputf, 'r', encoding='utf-8-sig') as fh:
    for line in fh:
        line = line.strip()

        line = "[[[[[9,8],1],2],3],4]"
        line = "[7,[6,[5,[4,[3,2]]]]]"
        line = "[[6,[5,[4,[3,2]]]],1]"
        line = "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"

        next_sfn = str2nested(line)

        print("Next nested line", next_sfn)

        if len(sfn) == 0:
            sfn = next_sfn
        else:
            sfn = [sfn, next_sfn]

        print(sfn)

        # now reduce if needed
        res = sfReduce(sfn)
        print(res[1])
        exit()


### Part 1
print("=========== PART 1 ===============")
print("Part 2 answer", 999)

### Part 2
print("=========== PART 2 ===============")
print("Part 2 answer", 999)
