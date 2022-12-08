import numpy as np

map = []
with open('input.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:

    for line in fh:
        l = line.strip('\n')
        map.append([x for x in l])

map = np.array(map, dtype=int)

print(map)

# go through map from each of the four directions and create a second 'map'
# of boolean visibility
visfl = np.zeros_like(map)
visfr = np.zeros_like(map)
visft = np.zeros_like(map)
visfb = np.zeros_like(map)

cmax = np.full(map.shape[1], -1, dtype=int)
cmax2 = np.full(map.shape[1], -1, dtype=int)
for r in range(map.shape[0]):

    # top down, left to right
    rmax = -1 
    for c in range(map.shape[1]):
        if map[r,c] > rmax:
            rmax = map[r,c]
            visfl[r,c] = 1
        if map[r,c] > cmax[c]:
            cmax[c] = map[r,c]
            visft[r,c] = 1

    # bottom up, left to right
    rmax = -1 
    r = map.shape[0] - r - 1 # reverse rows, from bottom up
    for c in reversed(range(map.shape[1])):
        if map[r,c] > rmax:
            rmax = map[r,c]
            visfr[r,c] = 1
        if map[r,c] > cmax2[c]:
            cmax2[c] = map[r,c]
            visfb[r,c] = 1

vis = (visfl + visfr + visfb + visft) > 0
print(vis)

# Part 1
print("#### Part 1 ####")
print("Part 1 answer: " + str(np.sum(vis)))
# 1822 wrong - too low - forgot about edges!

################################ PART 2 ######################
print('################################ PART 2 ######################')

# scenic score
ss = np.full(map.shape, -1, dtype=int)

# iterate through map/trees
for r in range(map.shape[0]):
    for c in range(map.shape[1]):

        # get the tree height
        th = map[r,c]

        # view distance: north, east, south, west
        vd = np.zeros(4, dtype=int)

        # look north
        tr = r - 1
        tc = c
        while tr >= 0:
            vd[0] += 1
            if map[tr,tc] >= th:
                break
            tr -= 1

        # look east
        tr = r
        tc = c + 1
        while tc < map.shape[1]:
            vd[1] += 1
            if map[tr,tc] >= th:
                break
            tc += 1

        # look south
        tr = r + 1
        tc = c
        while tr < map.shape[0]:
            vd[2] += 1
            if map[tr,tc] >= th:
                break
            tr += 1

        # look west
        tr = r
        tc = c - 1
        while tc >= 0:
            vd[3] += 1
            if map[tr,tc] >= th:
                break
            tc -= 1

        # calculate the scenic score
        ss[r,c] = np.prod(vd)

print(ss)

# Part 2
print("#### Part 2 ####")
print("Part 2 answer: " + str(np.max(ss)))
