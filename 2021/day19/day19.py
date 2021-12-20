import numpy as np
import math

input_file = 'test_input'
#input_file = 'input'

# scanners can detect beacons within 1000 units (x,y,z)
# scanners don't detect other scanners
# there are at least 12 beacons in common for each scanner pair
# xyz coordinates of beacons are relative to each scanner
# scanner is at 0,0,0

ubi = 0 # universal beacon identifier
class Scanner:

    def __init__(self, sn, beacons):
        global ubi

        self.sn = sn
        self.bnum = len(beacons)

        # universal_coordinate_system
        # set this scanner as using the 'universal' coordinate system 
        # others will get set to ucs as rotated
        if sn == 0:
            self.ucs = True
            self.location = [0,0,0]
        else:
            self.ucs = False
            self.location = None

        # build the dict of beacons
        self.beacons = {}
        for b in beacons:
            self.beacons[ubi] = b
            ubi += 1

        self.calcBeaconDistancesApart()

        # used for rolling to change coordinates directions
        self.rollXorRollZ = 'x'

    def __str__(self):
        print("Scanner number", self.sn)
        print("Detected", self.bnum, "beacons")
        print("Beacon coordinates:")
        print(self.beacons)
        print("Beacon interdistance matrix:")
        print(self.beacon_distance_matrix)
        return('End of beacon' + str(self.sn))

    def calcBeaconDistancesApart(self):
        b2bdist = []
        for b1id, b1xyz in self.beacons.items():
            for b2id, b2xyz in self.beacons.items():

                # calc distance from b1 to each b2
                p = pow(b1xyz[0] - b2xyz[0], 2)
                q = pow(b1xyz[1] - b2xyz[1], 2)
                r = pow(b1xyz[2] - b2xyz[2], 2)

                # 3D pythagorus
                b2bdist.append(math.sqrt(p + q + r))

        # convert list to well shaped matrix
        self.beacon_distance_matrix = np.array(b2bdist).reshape([self.bnum, self.bnum])

    def getDimDistribution(self, values):
        values = np.array(values, dtype=int)
        dmin = np.min(values)
        dmax = np.max(values)
        shifted = values - dmin
        return np.sort(shifted)

    def getBeaconIdsFromIndex(self, indices):
        return np.array(list(self.beacons.keys()), dtype=int)[indices]

    def getXYZDistributions(self, beacon_ids):
        #print("Sensor", self.sn, "beacons:", self.beacons)
        xyz_values = [xyz for bid, xyz in self.beacons.items() if bid in beacon_ids]

        x = [c[0] for c in xyz_values]
        y = [c[1] for c in xyz_values]
        z = [c[2] for c in xyz_values]

        #print(x,y,z)

        return [self.getDimDistribution(x), self.getDimDistribution(y), self.getDimDistribution(z)]

    def rollAxes(self):

        print(self.rollXorRollZ)

        # NO! There are 24 possibilities - 4 rotations for each 'heading'
        exit("FIX THIS")
        # Alternate rolls to test all 6 possibilities
        # only need to change coordinates of beacons
        if self.rollXorRollZ == 'x':
            print("Roll forwards")
            # Roll on X-axis forward
            self.rollXorRollZ = 'z'
            for bid, xyz in self.beacons.items():
                self.beacons[bid] = [xyz[0], xyz[2], -1*xyz[1]]
            return

        if self.rollXorRollZ == 'z':
            print("Roll right")
            # Roll on Z-axis right
            self.rollXorRollZ = 'x'
            for bid, xyz in self.beacons.items():
                self.beacons[bid] = [-1*xyz[1], xyz[0], xyz[2]]
            return


    def findDistMatches(self, s2):

        # ignore diagonal and below
        bdm  = self.beacon_distance_matrix
        bdm2 =   s2.beacon_distance_matrix

        s1h, s1w = bdm.shape
        s2h, s2w = bdm2.shape

        beacon_matches_ids = []
        for by in range(0, s1h-1):
            for bx in range(by+1, s1w):

                # now look in s2
                for b2y in range(0, s2h-1):
                    for b2x in range(b2y+1, s2w):
                        if bdm[by,bx] == bdm2[b2y,b2x]:
                            # this will match beacons with other beacons multiple times
                            beacon_matches_ids.append([by, bx, b2y, b2x])
                            #print("S1 Beacon", by, bx, "distance", bdm[by,bx])
                            #print("S2 Beacon", b2y, b2x, "distance", bdm2[b2y,b2x])

        # reduce the beacons to their respective sensor beacon ids
        bmi = np.array(beacon_matches_ids)
        # get the unique row/col ids of the beacons that appear in both scanner ranges
        # These are relative beacon ids - based on matrix col/row - translate to actual beacon ids
        s1bm = self.getBeaconIdsFromIndex(np.unique(bmi[:,0:2]))
        s2bm = s2.getBeaconIdsFromIndex(np.unique(bmi[:,2:4]))

        print("There are", len(s1bm), "matches between sensors", self.sn, "and", s2.sn)

        print("S1 beacons:", s1bm)
        gxd, gyd, gzd = self.getXYZDistributions(s1bm)
        print("Good distributions","\n", gxd, "\n", gyd,"\n", gzd)

        print("S2 beacons:", s2bm)
        axd, ayd, azd = s2.getXYZDistributions(s2bm)
        print("Alternate distributions","\n", axd,"\n", ayd,"\n", azd)

        rot_count = 0
        while not all(gxd == axd) or not all(gyd == ayd) or not all(gzd == azd):
            s2.rollAxes()
            axd, ayd, azd = s2.getXYZDistributions(s2bm)
            print("Alternate distributions","\n", axd,"\n", ayd,"\n", azd)
            rot_count += 1
            if rot_count > 5:
                exit("BAD ROTATION")

        print("SUCCESS")
        exit()

        # let's go through the list
        for s1bmi in s1bm:
            print("Sensor", self.sn, "'s beacon", s1bmi, "has a distance match with another beacon it sensed, equal to", s2.sn, "'s beacon detections")
            print(bmi[bmi[:,0] == s1bmi,:])

            # look at each sensor's pair, compare 



    
### Read input data
so = [] # scanner objects
with open(input_file, 'r', encoding='utf-8-sig') as fh:
    sn = None # scanner number
    beacons = []

    for line in fh:
        line = line.strip()

        if line == '':
            so.append(Scanner(sn, beacons.copy()))
            beacons = []
            continue

        if line[0:3] == '---':
            sn = int(line.split(' ')[2])
            continue

        beacons.append([int(n) for n in line.split(',')])
    # add last beacons to last scanner
    so.append(Scanner(sn, beacons))

# the plan is to rotate each scanner to conform with the first scanner (sn0)
for s1 in so:
    for s2 in so:
        if s1 != s2:
            # see which beacon distances s1 has with s2 they have in common
            s1.findDistMatches(s2)
            exit()

    

### Part 1
print("=========== PART 1 ===============")
print("Part 1 answer", 9999)

### Part 2
print("=========== PART 2 ===============")
print("Part 2 answer", 99999)
