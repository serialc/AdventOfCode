import numpy as np

input_file = 'test_input'
#input_file = 'test_input_larger'
#input_file = 'test_input_p2'
#input_file = 'input'

core = np.zeros([101,101,101], dtype=int)

instr = []
with open(input_file, 'r') as fh:
    for line in fh:
        line = line.strip()

        # turn on (1) or off (0) cuboid volumes
        on_or_off, xyz = line.split(' ')
        x,y,z = xyz.split(',')
        x = [int(v) for v in x[2:].split('..')]
        y = [int(v) for v in y[2:].split('..')]
        z = [int(v) for v in z[2:].split('..')]

        # for part 2
        instr.append([on_or_off, x,y,z])

        # check no part 2 instructions are processed here
        if (abs(x[0]) > 50 or abs(x[1]) > 50 or
            abs(y[0]) > 50 or abs(y[1]) > 50 or
            abs(z[0]) > 50 or abs(z[1]) > 50):
            # ingore
            continue

        # turning on cuboids
        if on_or_off == 'on':
            print("Turn on", x,y,z)
            for cx in range(50 + x[0], 50 + x[1] + 1):
                for cy in range(50 + y[0], 50 + y[1] + 1):
                    for cz in range(50 + z[0], 50 + z[1] + 1):
                        #print("on", cx,cy,cz)
                        core[cx,cy,cz] = 1
        else:
            # turning off cuboids
            print("Turn off", x,y,z)
            for cx in range(50 + x[0], 50 + x[1] + 1):
                for cy in range(50 + y[0], 50 + y[1] + 1):
                    for cz in range(50 + z[0], 50 + z[1] + 1):
                        #print("off", cx,cy,cz)
                        core[cx,cy,cz] = 0
        
##### PART 1 #####
# How many cubes are in the x=-50..50,y=-50..50,z=-50..50 core?
print("Part 1")
print("Final Core sum",np.sum(core))


##### PART 2 #####
# Way bigger cube, can't calculate through 3D volume of cells - too big/many
print("Part 2")

# don't create a full matrix
# just create list of descriptions of cuboids
# a cuboid is a 3D prism 
# each new cuboid impacts previous by splitting into new sub-cuboids.

class Cuboid:

    def __init__(self, xr,yr,zr):
        self.xrmin, self.xrmax = xr
        self.yrmin, self.yrmax = yr
        self.zrmin, self.zrmax = zr
        self.calcSum()

    def calcSum(self):
        self.sum = (
                (self.xrmax - self.xrmin + 1) *
                (self.yrmax - self.yrmin + 1) *
                (self.zrmax - self.zrmax + 1)
            )

    def checkForOverlap(self, newc):
        # Five possibilities * ~3 dimensions
        #1 --A---A----B---B----------
        #2 ------A----B-A-B----------
        #3 -----------BA-AB----------
        #4 -----------B-A-B---A------
        #5 -----------B---B--A----A--

        # deals with situations 1 and 5 above
        if ( (newc.xrmin > self.xrmax or newc.xrmax < self.xrmin) or 
            (newc.yrmin > self.yrmax or newc.yrmax < self.yrmin) or 
            (newc.zrmin > self.zrmax or newc.zrmax < self.zrmin) ):
            return ['no_overlap']

<<<<<<< HEAD
        # check if the new cuboid is contained within this one
        if ( (newc.xrmin <= self.xrmin and newc.xrmax <= self.xrmax)
            (newc.yrmin <= self.yrmin and newc.yrmax <= self.yrmax)
            (newc.zrmin <= self.zrmin and newc.zrmax <= self.zrmax) ):
            return ['contained']

        # now for all other situations split the incoming cuboid
        # check for clo

cuboids = []
for i in instr:
    print("Instruction set", i)

    # i = [on_or_off, x,y,z])
=======
        # For all others there is some overlap
        # need to split cuboid, modify self dimensions
        return True

    def splitSelf(self, ec):
        subc = []

        # we use the ec bounds, as these are the slicing values
        if ec.xrmin > (self.xrmin - 1) and ec.xrmin < (self.xrmax + 1):


# splitting concept is good, but not the lead up to that
def processAddedCuboid(c):
    global cuboids

    # check existing cuboids for overlap
    for ec in cuboids:
        if ec.checkForOverlap(c):
            # need to split the new cuboid (c) based on ec edges
            subc = c.splitSelf(ec)
            if len(subc) == 1:

            # for each subc, resubmit recursively to processAddedCuboid
            # until it only returns 1 item
            print(len(subc))
            exit()


cuboids = []
for i in instr:
    print(i)
>>>>>>> b4649c38421a9c28ea9c9d6de258440764192ae8

    if i[0] == 'on':
        # create new cuboid with volume 'on'
        c = Cuboid(i[1], i[2], i[3])
        # we split added cuboid to 'fit' deleting overlapping parts
        # c, and its potential splits, are added to the cuboids list
        processAddedCuboid(c)

    if i[0] == 'off':
        # create new cuboid with 'off' volume
        c = Cuboid(i[1], i[2], i[3])
        # we split existing cuboids to remove the overlap with c
        # c is not added to the list

<<<<<<< HEAD
        # check existing cuboids for overlap with cuboid c
        # need to split them, keep exclusive parts, don't duplicate volumes
        for ec in cuboids:
            ec.checkForOverlap(c)
=======
>>>>>>> b4649c38421a9c28ea9c9d6de258440764192ae8

    if i[0] == 'off':
        # convert existing cuboids portions to 'off'
        # by spliting them along the edges of this one
        # all existing 'on' cuboids
        # note any 'off' cuboid is deleted
        pass

