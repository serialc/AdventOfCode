import re
import numpy as np

input_file = 'input_test.txt'
#input_file = 'input_test2.txt'
input_file = 'input.txt'

# active (#) or inactive (.) state
# boot up by executing six cycles

cycles = 6
space = None # x,y,z,w
ss    = None # space size
isize = None # init size

with open(input_file, 'r') as fh:
    ypos = None
    zpos = None
    for line in fh:
        line = line.rstrip()

        if isize is None:
            isize = len(line)

            # existing width plus growth
            ss = isize + (cycles*2)

            #space =  np.arange(pow(gs, 3)).reshape((gs,gs,gs))
            # build the 3d 'space'
            space = np.chararray((ss,ss,ss,ss), itemsize=1)
            # to have it hold larger items:
            # space = np.chararray((ss,ss,ss), itemsize=5)

            # initialize with empty (of size/len 1)
            space[:] = '.'

        # we know that there are as many rows as col
        for i in range(len(line)):
            c = line[i]
            xpos = int(ss/2) - int(isize/2) + i
            if ypos is None:
                ypos = xpos
            if zpos is None:
                zpos = xpos

            space[xpos][ypos][zpos][int(ss/2)] = c

        ypos += 1

# display 3d space matrix
def viewspace():
    for w in range(ss):
        for z in range(ss):
            print('w=',w,'z=',z)
            for y in range(ss):
                for x in range(ss):
                    print(space[x,y,z,w].decode("utf-8"), end='')
                print()
            print()
        print()

# count active spaces
def countspace():
    spacen = 0
    print("SS=", ss)
    for w in range(ss):
        for z in range(ss):
            for y in range(ss):
                for x in range(ss):
                    if space[x, y, z,w] == b'#':
                        spacen += 1
    return spacen

# count neighbours in 3d space
def count_neighbours(tx,ty,tz,tw):
    global space
    nnum = 0
    for w in range(-1,2):
        for z in range(-1,2):
            for y in range(-1,2):
                for x in range(-1,2):
                    if x == 0 and y == 0 and z == 0 and w == 0:
                        # don't count yourself
                        continue
                    try:
                        if space[tx + x, ty + y, tz + z, tw + w] == b'#':
                            nnum += 1
                    except IndexError:
                        # normal for edges
                        continue
    return nnum

def step():
    global space
    nextspace = space.copy()

    # check all space - not efficient as we grow from the core ...
    for w in range(ss):
        for z in range(ss):
            for y in range(ss):
                for x in range(ss):
                    if space[x][y][z][w] == b'#':
                        ncount = count_neighbours(x,y,z,w)
                        if ncount != 2 and ncount != 3:
                            # remove/deactivate
                            nextspace[x][y][z][w] = '.'
                    if space[x][y][z][w] == b'.':
                        ncount = count_neighbours(x,y,z,w)
                        if ncount == 3:
                            # activate
                            nextspace[x][y][z][w] = '#'

    space = nextspace.copy()

# iterate!
for cnum in range(cycles):
    print("Cycle", cnum+1)
    step()

viewspace()

print("Part 1 - Number of active cubes is", countspace())
