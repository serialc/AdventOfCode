import numpy as np
from PIL import Image

inputf = 'test_input'
inputf = 'test_input2' # part2 fails for this input - why?
inputf = 'test_input3'
inputf = 'input'

net = {}
### Read input data
with open(inputf, 'r') as fh:
    for line in fh:
        line = line.strip()
        o,d = line.split('-')
        if o not in net:
            net[o] = [d]
        else:
            net[o].append(d)

        # Add bidirectionality
        if d != 'end' and o != 'start':
            if d not in net: 
                net[d] = [o]
            else:
                net[d].append(o)

# recursive func
def findEnd(path, o, mode, doubledVisitedSmall):

    global finished_paths

    new_path = path.copy()
    new_path.append(o)

    if o == 'end':
        finished_paths.append(new_path)
        return

    # Check each possible destination
    for d in net[o]:

        if mode == 1:
            if d.islower() and d in new_path:
                # don't go to small caves we've been to already
                continue
            findEnd(new_path, d, mode, False)

        if mode == 2:

            # already visited this small cave and another
            if d.islower() and d in new_path and doubledVisitedSmall:
                continue

            # first small cave we're visiting twice
            if d.islower() and d in new_path and not doubledVisitedSmall:
                findEnd(new_path, d, mode, True)
                continue

            # large cave or first visit to small cave
            findEnd(new_path, d, mode, doubledVisitedSmall)
    
finished_paths = []
for d in net['start']:
    findEnd(['start'], d, 1, False)

### Part 1
print("\n###### Part 1")
print("Number of paths through caves", len(finished_paths))

### Part 2
print("\n###### Part 2")

finished_paths = []
for d in net['start']:
    findEnd(['start'], d, 2, False)

print("Number of paths through caves", len(finished_paths))
