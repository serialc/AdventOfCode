import numpy as np

def matPrint(mat, sep=''):
    nh,nw = mat.shape
    for y in range(nh):
        for x in range(nw):
            if len(str(mat[y,x])) == 1:
                print(' ', end='')
            print(str(mat[y,x]) + sep, end='')
        print()
    print()

def getValidNeighbour(c, m, d):
    y,x = c
    v = m[c[0], c[1]]
    mh,mw = m.shape
    valid = []

    # above
    if y - 1 >= 0 and d[y-1, x] != 0:
        aval = m[y-1, x]
        adiff = v - aval
        if adiff < 2:
            valid.append(d[y-1, x])

    # right
    if x + 1 < mw and d[y, x+1] != 0:
        rval = m[y, x+1]
        rdiff = v - rval
        if rdiff < 2:
            valid.append(d[y, x+1])

    # below
    if y + 1 < mh and d[y+1, x] != 0:
        bval = m[y+1, x]
        bdiff = v - bval
        if bdiff < 2:
            valid.append(d[y+1, x])

    # left
    if x - 1 >= 0 and d[y, x-1] != 0:
        lval = m[y, x-1]
        ldiff = v - lval
        if ldiff < 2:
            valid.append(d[y, x-1])

    if len(valid) == 0:
        return False

    return min(valid)


emap = []
with open('input.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:

    start = []
    end = []
    r = 0
    for line in fh:
        l = line.strip('\n')
        emap.append([ord(x)-96 for x in l])

        s = l.find('S')
        if l.find('S') != -1:
            start = [r,s]
        e = l.find('E')
        if l.find('E') != -1:
            end = [r,e]

        r += 1

emap = np.array(emap, dtype=int)
# fix start/end
emap[start[0], start[1]] = 1
emap[end[0], end[1]] = np.max(emap)

def getDistanceFromLoc(start, emap, show_maps=False):

    # make a same sized map to elevation but for path distance
    dist = np.zeros_like(emap)
    dist[start[0], start[1]] = 1

    if show_maps:
        print('elevation')
        matPrint(emap, ' ')

        print('distance from start')
        matPrint(dist, ' ')

    while True:
        changes = False
        mh,mw = emap.shape
        for y in range(mh):
            for x in range(mw):
                if dist[y,x] != 0:
                    continue
                ret = getValidNeighbour([y,x], emap, dist)
                if ret is not False:
                    changes = True
                    dist[y,x] = ret + 1

        if not changes:
            if show_maps:
                matPrint(dist, ' ')
            break

    if show_maps:
        matPrint(dist, ' ')
    return dist[end[0], end[1]] - 1


# Part 1
print("#### Part 1 ####")
print("Part 1 answer: " + str(getDistanceFromLoc(start, emap)))

################################ PART 2 ######################
print('################################ PART 2 ######################')

aresults = []
mh,mw = emap.shape
for y in range(mh):
    for x in range(mw):
        if emap[y,x] == 1:
            res = getDistanceFromLoc([y,x], emap)
            if res != -1:
                aresults.append(res)
                print(y,x,aresults)

print(aresults)

# Part 2
print("#### Part 2 ####")
print("Part 2 answer: " + str(min(aresults)))
