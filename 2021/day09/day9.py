import numpy as np

inputf = 'test_input'
inputf = 'input'

# get coords in readable
sfmap = []
# assume 0,0 is min
with open(inputf, 'r') as fh:
    for line in fh:
        line = line.strip()
        sfmap.append(list(line))

sfmap = np.array(sfmap, dtype=int)
smokeloc = []
smokemap = np.zeros(sfmap.shape, dtype=int)

height, width = np.shape(sfmap)
print("height", height, "width", width)

def getVonNeumannNeighbours(surface, y,x):
    n = []
    if y != 0:
        n.append(surface[y-1, x])
    if x != 0:
        n.append(surface[y, x-1])
    if y != (height-1):
        n.append(surface[y+1, x])
    if x != (width-1):
        n.append(surface[y, x+1])

    return np.array(n, dtype=int)


def getMooreNeighbours(surface, y,x):
    # fix edge cases

    # top left corner
    if y == 0 and x == 0:
        return surface[y:y+2, x:x+2]

    # bottom right corner
    if y == (height-1) and x == (width-1):
        return surface[y-1:y+1, x-1:x+1]

    # top right corner
    if y == 0 and x == (width-1):
        return surface[y:y+2, x-1:x+1]

    # bottom left corner
    if y == (height-1) and x == 0:
        return surface[y-1:y+1, x:x+2]

    # bottom
    if y == (height-1):
        return surface[y-1:y+1, x-1:x+2]

    # right
    if x == (width-1):
        return surface[y-1:y+2, x-1:x+1]

    # top
    if y == 0:
        return surface[y:y+2, x-1:x+2]

    # left
    if x == 0:
        return surface[y-1:y+2, x:x+2]

    # return normal 3x3 matrix
    return surface[y-1:y+2, x-1:x+2]

#### Part 1 ####
for y in range(height):
    for x in range(width):
        val = sfmap[y,x]
        #subm = getMooreNeighbours(sfmap, y,x)
        subm = getVonNeumannNeighbours(sfmap, y,x)

        # is a low point if
        # - val is less than the minimum value in the neighbourhood

        if np.min(subm) > val:
            smokeloc.append([y,x,val])
            smokemap[y,x] = 1

smokeloc = np.array(smokeloc)

print("Part 1 answer is", np.sum(smokeloc[:,2:3]+1))

#### Part 2 ####
print("\nPart 2")

basins = np.zeros(np.shape(sfmap), dtype=int)

# initialize hot spots
for i in range(np.shape(smokeloc)[0]):
    y,x = smokeloc[i][0:2]
    basins[y,x] = i+1

#print(basins)

# let's use CA
changed = True
while changed:
    changed = False
    for y in range(height):
        for x in range(width):

            # if basin location is already coded or
            # it is a ridge on the seafloor map go
            # then skip
            if basins[y,x] != 0 or sfmap[y,x] == 9:
                continue

            n = getVonNeumannNeighbours(basins, y,x)
            noridge = n[n != 9]
            hotzone = n[n != 0]
            if len(hotzone) > 0:
                #print(y,x,"is in",hotzone[0])
                changed = True
                # we will never have two different values, just choose the first
                basins[y,x] = hotzone[0]



print(basins)

# sort results
basinids, basinsize = np.unique(basins, return_counts=True)
results = np.asarray((basinids, basinsize)).T
results_sorted = results[results[:, 1].argsort()][::-1]

print("Part 2 answer is", np.prod(results_sorted[1:4,1]))

#### Bonus ####
print("Generating image")

from PIL import Image

magnification = 4
im = Image.new('RGB', (width*magnification, height*magnification))

pixellist = []
for y in range(height):
    # double pixel vertical
    for i in range(magnification):
        for x in range(width):
            # double pixel width
            for j in range(magnification):
                if smokemap[y,x] == 1:
                    pixellist.append((255,0,0))
                    continue
                val = sfmap[y,x]
                if val == 9:
                    # black ridge
                    pixellist.append((0,0,0))
                else:
                    pixellist.append((27 + int(81/9 * (9-val)), int(27/9*val), int(27/9*val)))

im.putdata(pixellist)
im.save('ridges_seafloor.png')
