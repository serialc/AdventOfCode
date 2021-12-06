import numpy as np

inputf = 'test_input'
inputf = 'input'

# get coords in readable
flistclean = []
# assume 0,0 is min
with open(inputf, 'r') as fh:
    for line in fh:
        line = line.strip()
        flistclean = np.array([int(x) for x in line.split(',')], dtype=int)

dproj = 80 # part 1
flist = flistclean.copy()

for d in range(1,dproj+1):
    nfish = np.sum(flist == 0)
    #print("New fish: " + str(nfish))

    # age by 1 day (goes down)
    flist = flist - 1
    flist[flist == -1] = 6
    flist = np.append(flist, [8] * nfish)
    
    #print("After " + str(d) + " day:", flist)
    #print("Number of fish after day ", d , " is ", len(flist))

print("Part 1 answer is", len(flist))

#### Part 2 ####
# technique doesn't work for big numbers
# regroup into dicts with number of fish of each age!

dproj = 256 # part 2
#dproj = 18 # part 2
flist = flistclean.copy()

# restruct flist into dict
fdict = {}
for f in flist:
    if f in fdict:
        fdict[f] += 1
    else:
        fdict[f] = 1
#print(fdict) #good

for d in range(1,dproj+1):
    print("Day ", d)
    # next iteration
    nfdict = {}
    nfish = 0

    # age by 1 day (goes down)
    for dl, num in fdict.items():
        if dl == 0:
            # careful not to overwrite
            if 6 in nfdict:
                nfdict[6] += num
            else:
                nfdict[6] = num

            # add new fish
            nfdict[8] = num
            print("New fish: " + str(num))
        else:
            if dl-1 in nfdict:
                nfdict[dl-1] += num
            else:
                nfdict[dl-1] = num
    
    # overwrite
    fdict = nfdict.copy()

#print("After " + str(d) + " day:", flist)
print("Number of fish after day ", d , " is ", sum(fdict.values()))

