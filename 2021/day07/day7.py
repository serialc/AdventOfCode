import numpy as np

input = 'test_input'
input = 'input'

pos = []
with open(input, 'r') as fh:
    for line in fh:
       pos = np.array(line.strip().split(','), dtype=int)

def posCost(i):
    return np.sum(np.abs(pos - i))

costDict = {}
def posCost2(i):
    global costDict
    dists = np.abs(pos - i)
    cfuel = [np.sum(nCumSum(x)) for x in dists]
    costDict[i] = np.sum(cfuel)
    return costDict[i]

def nCumSum(n):
    return int((n+1)*n/2)

#### The smart way #######

# part 1
print(posCost(int(np.median(pos))))
# part 2
print(posCost2(int(np.mean(pos))))


#### My rush-forward without thinking what I'm doing way #########

# part 1
mincost = False
minindex = 0
print("Mean is: ", np.mean(pos))
print("Median is: ", np.median(pos))
for i in range(np.min(pos), np.max(pos) + 1):
    icost = posCost(i)
    if not mincost:
        mincost = icost
    if icost < mincost:
        mincost = icost
        minindex = i

print("Part 1")
print("Loc ", minindex , " cost is ", mincost)

# part 2
print("Part 2")


mincost = False
minindex = 0

# start search at median or mean?
i = int(np.mean(pos))
# assume no local minumum?
while(True):
#for i in range(np.min(pos), np.max(pos) + 1):
    # get costs of this index and above
    if i not in costDict.keys():
        posCost2(i)
    if i+1 not in costDict.keys():
        posCost2(i+1)

    # compare them
    if costDict[i] < costDict[i+1]:
        # get fuel cost of index below
        if i-1 not in costDict.keys():
            posCost2(i-1)

        # check if index below is better
        if costDict[i-1] > costDict[i]:
            mincost = costDict[i]
            minindex = i
            break
        else:
            # jump 2 as we already know i and i-1 comparison
            i = i-2
    else:
        i = i+1
    #if icost < mincost:
        #mincost = icost
        #minindex = i
print("Loc ", minindex , " cost is ", mincost)
# oh my god, it's just the mean floored?
print(costDict)
