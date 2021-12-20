import numpy as np
import math

input_file = 'test_input'
input_file = 'input'

### Functions

def getThreeByThree(y,x,mat):
    # we will only ever ask this for locations that
    # have the full neighbourhoods possible
    h,w = mat.shape

    # need to imagine infinity, careful!
    # if on edge
    if x == 0 or y == 0 or x == (w-1) or y == (h-1):
        #imagine all neighbours are the same as me
        return np.array(np.repeat(mat[y,x],9), dtype=int)

    else:
        return mat[y-1:y+2, x-1:x+2]

def getMatCode(y,x,mat):
    nine = getThreeByThree(y,x,mat)
    nine = ''.join([str(x) for x in nine.flatten()])
    return int(nine, 2)

def cycleThrough(mat):
    h,w = mat.shape
    newmat = np.zeros(mat.shape, dtype=int)

    # ignore edges
    for y in range(h):
        for x in range(w):

            # get 3x3 code
            code = getMatCode(y,x,mat)
            newmat[y,x] = iea[code]

    return newmat

def printMat(mat):
    h,w = mat.shape
    for y in range(h):
        for x in range(w):
            if mat[y,x] == 1:
                print("#", end='')
            else:
                print(".", end='')
        print()
    print()

### Read input data

iea = None
img = []
with open(input_file, 'r', encoding='utf-8-sig') as fh:
    for line in fh:
        line = line.strip()

        if line == "":
            continue

        if iea is None:
            iea = np.array([x == '#' for x in list(line)], dtype=int)
            continue

        img.append([x == '#' for x in list(line)])


img = np.array(img, dtype=int)
#print(img)
#print(iea)

def iterateProcess(cycles, srcimg):
    bsize = img.shape[0]
    edge_buffer = 10
    edge = cycles + edge_buffer + 1
    # for each cycle we need 1 extra cell for each side (x2) plus one additional on each edge for 3x3 filter
    lsize = bsize + edge * 2
    limg = np.zeros([lsize, lsize], dtype=int)

    # insert img into limg
    limg[edge:edge+bsize, edge:edge+bsize] = img
    printMat(limg)

    # iterate
    for i in range(cycles):
        limg = cycleThrough(limg)
        printMat(limg)

    return np.sum(limg)

### Part 1
pixelnum = iterateProcess(2, img.copy())

print("=========== PART 1 ===============")
print("Part 1 answer", pixelnum)
# first guess 6513
# second guess 5425
# third guess 5326 [correct]

### Part 2
print("=========== PART 2 ===============")
pixelnum = iterateProcess(50, img.copy())
print("Part 2 answer", pixelnum)
