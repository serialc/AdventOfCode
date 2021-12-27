import numpy as np

input_file = 'test_input'
input_file = 'test_input_larger'
input_file = 'test_input_p2'
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
        
##### PART 2 #####
# How many cubes are in the x=-50..50,y=-50..50,z=-50..50 core?
print("Part 1")
print("Final Core sum",np.sum(core))

##### PART 2 #####
print("Part 2")

# don't create a full matrix, just sections, each new cuboid impacts previous

class Cuboid:

    def __init__(self, xr,yr,zr):
        self.xrmin, self.xrmax = xr
        self.yrmin, self.yrmax = yr
        self.zrmin, self.zrmax = zr
        self.sum = (
                (xrmax - xrmin + 1) *
                (yrmax - yrmin + 1) *
                (zrmax - zrmax + 1)
                )

    def checkForOverlap(self, newc):
        # Five possibilities * 3
        #1 --A---A----B---B----------
        #2 ------A----B-A-B----------
        #3 -----------BA-AB----------
        #4 -----------B-A-B---A------
        #5 -----------B---B--A----A--

        # deals with situations 1 and 5 above
        if ( (newc.xrmin > self.xrmax or newc.xrmax < self.xrmin) or 
            (newc.yrmin > self.yrmax or newc.yrmax < self.yrmin) or 
            (newc.zrmin > self.zrmax or newc.zrmax < self.zrmin) ):
            return False

        # check for clo

cuboids = []
for i in instr:
    print(i)
    if i[0] == 'on':
        # create new cuboid with 'on' volume
        c = Cuboid(i[1], i[2], i[3])

        # check existing cuboids for overlap
        for ec in cuboids:
            ec.checkForOverlap(c)


