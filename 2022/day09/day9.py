import numpy as np

def printMap(surf, nodes, points=True):
    for r in reversed(range(surf.shape[0])):
        for c in range(surf.shape[1]):
            if np.all([c,r] == nodes[0,]):
                print('H', end='')
            elif np.all([c,r] == nodes[len(nodes)-1,]):
                print('T', end='')
            else:
                found = False
                for n in range(1, nodes.shape[0]-1):
                    if np.all([c,r] == nodes[n,]):
                        print(n, end='')
                        found = True

                if not found:
                    if points:
                        print('.', end='')
                    else:
                        print(surf[r,c], end='')
        # newline
        print()
    print()

with open('input.txt', 'r') as fh:
#with open('test_input2.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:

    cmax = np.zeros(4, dtype=int)
    x = 0
    y = 0
    instr = []
    for line in fh:
        l = line.strip('\n')
        d,c = l.split(' ')
        c = int(c)
        instr.append([d,c])

        # update location
        if d == 'R':
            x += c
        if d == 'L':
            x -= c
        if d == 'U':
            y += c
        if d == 'D':
            y -= c

        # check max coordinates
        if y > cmax[0]:
            cmax[0] = y
        if x > cmax[1]:
            cmax[1] = x
        if y < cmax[2]:
            cmax[2] = y
        if x < cmax[3]:
            cmax[3] = x
        print(x,y)

shape = [1 + cmax[0] - cmax[2], 1 + cmax[1] - cmax[3]]
# need to start in the middle, not a corner otherwise we go off map
startpos = np.flip(np.abs(cmax[2:4]))

#print("start=0,0")
#print("end=",x,",",y)
#print("maxbounds=", cmax)
#print("shape=", shape)
#print(instr)
#print(startpos)

### start the movement

def flailTail(dim, tlen):
    tmap = np.zeros(shape, dtype=int)

    # make locations np so we can perform operations on them
    n = np.full([tlen, 2], startpos, dtype=int)

    # track the start locations on the map
    tmap[0,0] += 1

    # CAREFUL - the location tuples are [x,y] while the map is [y,x]!

    for i in instr:
        d,c = i
        print("Instruction: ",d,c)

        while c > 0:
            # move head
            if d == 'R':
                n[0,0] += 1
            if d == 'L':
                n[0,0] -= 1
            if d == 'U':
                n[0,1] += 1
            if d == 'D':
                n[0,1] -= 1

            for tid in range(1, tlen):
                # check if the tail(s) needs to be updated
                ht_diff = n[tid-1,] - n[tid,] 
                ht_abdiff = np.abs(ht_diff)
                dist = np.sum(ht_abdiff)
                #print(tid, ht_diff, ht_abdiff, dist)

                # is the head too far?
                if dist > 1:
                    # but is it in a corner - one away?
                    if ht_abdiff[0] == ht_abdiff[1] and ht_abdiff[0] == 1:
                        # it's diagonally adjacent
                        pass
                    else:
                        # it's too far away - but in which direction?
                        if ht_diff[0] == 0:
                            # same x-value, so same column - move up/down
                            n[tid,1] += 1 * np.sign(ht_diff[1])
                        elif ht_diff[1] == 0:
                            # same y-value, so same row - move left/right
                            n[tid,0] += 1 * np.sign(ht_diff[0])
                        else:
                            # it's not in column or row - need to move diagonally
                            n[tid,0] += 1 * np.sign(ht_diff[0])
                            n[tid,1] += 1 * np.sign(ht_diff[1])

                        # Is this the tail?
                        if tid == tlen-1:
                            # the tail has moved, update the tail map
                            tmap[n[tid,1], n[tid,0]] += 1

            # complete one step
            #printMap(tmap, n, True)
            c -= 1

    #print("Final Head Map")
    print("Final Tail Map")
    printMap(tmap, n, False)

    return tmap

tmap2 = flailTail(shape, 2)

# Part 1
print("#### Part 1 ####")
print("Part 1 answer: " + str(np.sum(tmap2 > 0)))

################################ PART 2 ######################
print('################################ PART 2 ######################')

tmap10 = flailTail(shape, 10)

# Part 2
print("#### Part 2 ####")
print("Part 2 answer: " + str(np.sum(tmap10 > 0)))
# guess 2494, too low
