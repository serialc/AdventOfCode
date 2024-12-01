#from math import prod
import numpy as np
import re

input_file = 'input0'
input_file = 'input'

laststate = ''
state = ''
statevalues = dict()
maps = []

def mapTransition (val):
    for thismap in maps:
        if val in range(thismap[1], thismap[1] + thismap[2]):
            # map index + last index within range
            return thismap[0] + (val - thismap[1])
    return val

with open(input_file, 'r') as fh:
    for l in fh:
        l = l.strip('\n')

        if 'seeds' in l:
            state = 'seed'
            statevalues[state] = list(map(int, l.split(': ')[1].split(' ')))
            continue

        if l == '':
            if laststate != '':
                # apply the mapping for this state from the laststate
                for v in statevalues[laststate]:
                    statevalues[state].append(mapTransition(v))

                # reset the maps
                maps = []
            continue

        if 'map' in l:
            laststate = state
            state = l.split(' ')[0].split('-to-')[1]
            statevalues[state] = []
            continue

        # only lines with numbers get here
        # save the mapping
        maps.append(list(map(int, l.split(' '))))


# need to run last transition
for v in statevalues[laststate]:
    statevalues[state].append(mapTransition(v))
print(statevalues)

print("#### Part 1 ####")
print("Answer is:", min(statevalues[state]))

#### PART 2 ####
print("============ Part 2 start ================")

# reset everything
laststate = ''
state = ''
statevalues = dict()
maps = []

def mapTransition2 (valr):

    # valr is a tuple containing [MIN, MAX]
    # note that valr may span multiple maps!
    # and we'll need to split it
    taskstack = [valr]
    retpackage = []

    while len(taskstack) > 0:
        task = taskstack.pop()
#        print('Task', task)

        task_processed = False
        for thismap in maps:
#            print('Map', thismap)

            # maps are in the form
            # DST, SRC, SPAN
            # get the bounds of this mapping limits 
            rmin = thismap[1]
            rmax = thismap[1] + thismap[2]

            # if an easy one, append to task list vranges
            if task[0] >= rmin and task[1] < rmax:
                #print('A')
                retpackage.append([
                    thismap[0] + (task[0] - thismap[1]),
                    thismap[0] + (task[1] - thismap[1])
                ])
                task_processed = True
                continue

            # Harder ones
            # need to chop up the task and map them
            # intervene in three situations
            # -----X---vvXvv----
            # ---vvXvv---X------
            # ---vvXvvvvvXvv----
            if task[0] >= rmin and task[0] < rmax and task[1] >= rmax:
                #print('B')
                retpackage.append([
                    thismap[0] + (task[0] - thismap[1]),
                    thismap[0] + thismap[2]
                ])
                taskstack.append([rmax, task[1]])
                task_processed = True
                continue

            if task[0] < rmin and task[1] > rmin and task[1] < rmax:
                #print('C')
                taskstack.append([task[0], rmin])
                retpackage.append([
                    thismap[0],
                    thismap[0] + (task[1] - thismap[1])
                ])
                task_processed = True
                continue

            if task[0] < rmin and task[1] > rmax:
                #print('D')
                taskstack.append([task[0], rmin])
                retpackage.append([rmin, rmax])
                taskstack.append([rmax, task[1]])
                task_processed = True
                continue

        # task not in either map
        # return as is
        if not task_processed:
            # doesn't fall within either maps
            retpackage.append(task)

    #print("Returned", retpackage)
    return retpackage

with open(input_file, 'r') as fh:
    for l in fh:
        l = l.strip('\n')

        if 'seeds' in l:
            state = 'seed'
            statevalues[state] = []
            p2ranges = list(map(int, l.split(': ')[1].split(' ')))
            for pi in range(int(len(p2ranges)/2)):
                # store the range pair - change from [START, LENGTH] to [MIN, MAX]
                statevalues[state].append([p2ranges[pi*2], p2ranges[pi*2] + p2ranges[pi*2 + 1] - 1])
            print(statevalues)
            continue

        if l == '':
            if laststate != '':
                # apply the mapping for this state from the laststate
                for vr in statevalues[laststate]:
                    statevalues[state].extend(mapTransition2(vr))

                # reset the maps
                maps = []
            continue

        if 'map' in l:
            laststate = state
            state = l.split(' ')[0].split('-to-')[1]
            statevalues[state] = []
            continue

        # only lines with numbers get here
        # save the mapping
        maps.append(list(map(int, l.split(' '))))

# need to run last transition
for vr in statevalues[laststate]:
    statevalues[state].extend(mapTransition2(vr))
print(statevalues)

print("#### Part 2 ####")
print("Answer is:", min([x[0] for x in statevalues[state]]))
