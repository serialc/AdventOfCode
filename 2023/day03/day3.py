import numpy as np

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

input_file = 'input0'
input_file = 'input'

parts = []
symbols = []
smatrix = []

### Read input data
with open(input_file, 'r') as fh:

    y = 0
    for line in fh:

        line = line.strip()
        if line == "":
            continue

        # gobble the line
        plist = []
        slist = []
        smlist = []

        i = 0

        while i < len(line):

            # populate the parts
            if line[i].isdigit():
                plist.append(int(line[i]))
                slist.append(False)
                smlist.append('')
                i += 1
                continue

            if line[i] == '.':
                plist.append(None)
                slist.append(False)
                smlist.append('')
                i += 1
                continue
            
            # this is a symbol - populate the symbols 
            plist.append(None)
            slist.append(True)
            smlist.append(line[i])
            i += 1

        parts.append(plist)
        symbols.append(slist)
        smatrix.append(smlist)

        # end of processing a line
    # end of file access

parts = np.array(parts)
symbols = np.array(symbols)
smatrix = np.array(smatrix)
print(smatrix)

# get the numbers (not just digits) and their bounds
numdict = {}
for y in range(parts.shape[0]):
    number = ''
    for x in range(parts.shape[1]):
        pv = parts[y][x]
        if pv is not None:
            number += str(pv)
            continue
        if number != '':
            numdict['y' + str(y) + 'x' + str(x) + '_' + number] = [y, x-1, y, x-(len(number))]
            number = ''

    # catch any number against the right side / end of line
    if number != '':
        numdict['y' + str(y) + 'x' + str(x) + '_' + number] = [y, x-1, y, x-(len(number))]

print(numdict)
vparts = []
vcells = []

# buffer the numbers and check bounds to see if a part is present (can't exceed map area)
for num, bounds in numdict.items():

    ylim, xlim = parts.shape
    
    # buffer
    bounds[0] -= 1
    bounds[1] += 1
    bounds[2] += 1
    bounds[3] -= 1

    # constrain to map bounds
    if bounds[0] < 0:
        bounds[0] = 0
    if bounds[1] >= xlim:
        bounds[1] = xlim - 1
    if bounds[2] >= ylim:
        bounds[2] = ylim - 1
    if bounds[3] < 0:
        bounds[3] = 0

    # see if there are any symbols in these bounds
    # subset the symbols matrxi according to the given bounds
    symarea = symbols[bounds[0]:bounds[2]+1,bounds[3]:bounds[1]+1]
    
    if np.any(symarea):
        print(num, " is valid with bounds ", bounds)
        vparts.append(int(num.split('_')[1]))

        # save the valid bounds
        vcells.append(bounds)

for y in range(parts.shape[0]):
    for x in range(parts.shape[1]):

        tcol = bcolors.FAIL;
        for b in vcells:
            if y >= b[0] and x <= b[1] and y <= b[2] and x >= b[3]:
                tcol = bcolors.OKGREEN
                break;

        if symbols[y][x]:
            print(tcol + smatrix[y][x] + bcolors.ENDC, end='')
            continue

        if parts[y][x] is None:
            print(tcol + '.' + bcolors.ENDC, end='')
        else:
            print(tcol + str(parts[y][x]) + bcolors.ENDC, end='')
    print()

print("###### PART 1 Answer #########")
print(sum(vparts))
# Attempt 1: 311644 is too low

# Some numbers are present more than once! I was overwritting the dict with later values!
# I added x/y coordinates to the start of the dict key - should always check that dict item doesn't exist! 
# Attempt 2: 528819

print("=========== PART 2 START ===========")

slpairs = {}

for num, b in numdict.items():
    # get the buffer bounds and apply to the symbols matrix
    gears = smatrix[b[0]:b[2]+1,b[3]:b[1]+1]

    # find the coordinate of the top-left corner of the buffer area
    partnum = num.split('_')[1]
    yxloc = num.split('_')[0][1:].split('x')
    yxloc = [int(z) for z in yxloc]

    # determine the top/left coordinate of the buffer
    if yxloc[0] > 0:
        yxloc[0] -= 1
    yxloc[1] -= len(partnum) + 1
    if yxloc[1] < 0:
        yxloc[1] = 0

    # need to identify the location of the symbol

    if (gears == '*').any():
        # get the location of the symbole within the buffer space
        mloc = np.squeeze(np.asarray(np.where(gears == '*')))
        # add this to our buffer coordinate
        symloc = yxloc + mloc
        key = str(symloc[0]) + '_' + str(symloc[1])

        if key in slpairs:
            slpairs[key].append(partnum)
        else:
            slpairs[key] = [partnum]

        #print(num)
        #print(yxloc)
        #print(partnum)
        #print(gears)

print(slpairs)

parts_sum = 0
for pp in slpairs.values():
    if len(pp) == 2:
        print(pp)
        parts_sum += int(pp[0]) * int(pp[1])


print("###### PART 2 Answer #########")
print(parts_sum)
