import numpy as np
import math

input_file = 'test_input'
input_file = 'input'

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
        self.rollDim = 1

    def __str__(self):
        print("Scanner number", self.sn)
        print("Detected", self.bnum, "beacons")
        print("Beacon coordinates:")
        print(self.beacons)
        print("Beacon interdistance matrix:")
        print(self.beacon_distance_matrix)
        return('End of beacon' + str(self.sn))

    def setUCS(self):
        # uses the 'correct' coordinates system now
        self.ucs = True

    def getBeaconCoords(self, bid):
        return np.array(self.beacons[bid], dtype=int)

    def shiftAllBeaconLocationsToUCS(self):
        # use the already set self.location for the shift to UCS
        print("Sensor", self.sn, "UCS location is", self.location)
        for bid, xyz in self.beacons.items():
            self.beacons[bid] = np.array(xyz) + self.location
            #print(self.beacons[bid])

    def updateBeaconIdsTo(self, source_sensor):
        # go through my sensors and change their id to that of the source_sensor
        bid2delete = []
        bid2add = []
        for bid, xyz in self.beacons.items():
            for sbid, sxyz in source_sensor.beacons.items():
                if all(np.array(xyz) == np.array(sxyz)):
                    # 'add' beacon to self
                    bid2add.append(sbid)
                    # delete old beacon
                    bid2delete.append(bid)

        for bid in bid2delete:
            #print("Deleted bid", bid)
            del self.beacons[bid]
        for sbid in bid2add:
            self.beacons[sbid] = source_sensor.beacons[sbid]

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

        self.rollDim += 1

        # change coordinates of beacons
        #print("Roll dimension", self.rollDim)

        #print("Rotate clockwise (on Y-axis)")
        for bid, xyz in self.beacons.items():
            # 3D transform
            self.beacons[bid] = [xyz[2], xyz[1], -1*xyz[0]]

        # ! There are 24 possibilities - 4 rotations for each 'heading'
        # Alternate rolls to test all 6 possibilities
        if self.rollDim % 8 == 0:
            #print("Roll forwards (on X-axis)")
            # Roll on X-axis forward
            for bid, xyz in self.beacons.items():
                # 3D transform
                self.beacons[bid] = [xyz[0], xyz[2], -1*xyz[1]]
            return

        if self.rollDim % 4 == 0:
            #print("Roll right (on Z-axis)")
            # Roll on Z-axis right
            for bid, xyz in self.beacons.items():
                # 3D transform
                self.beacons[bid] = [-1*xyz[1], xyz[0], xyz[2]]
            return

    def findDistMatches(self, s2):

        print("\nLooking for beacon matches between Sensor numbers", self.sn, s2.sn)

        # ignore diagonal and below
        bdm  = self.beacon_distance_matrix
        bdm2 =   s2.beacon_distance_matrix
        #print(bdm)
        #print(bdm2)

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

        if len(bmi) == 0:
            #print("There are no matches between sensors", self.sn, "and", s2.sn)
            return

        # it should actually be fairly easy to match the sensors ids using
        # bmi
        #print("bmi\n",bmi)

        bm1v, bm1f = np.unique(bmi[:,:2], return_counts=True)
        #print(bm1v,"\n",bm1f)
        match_dict = {}
        for i in range(len(bm1v)):
            m1 = bm1v[i]

            # ignore infrequent matches
            if bm1f[i] < 11:
                return

            # get the s2 beacon ids that match 11+ times with m1
            bm2set = bmi[(bmi[:,0:2] == m1).any(axis=1), 2:]
            bm2v, bm2f = np.unique(bm2set, return_counts=True)
            #print(bm2v, "\n", bm2f)
            for j in range(len(bm2v)):
                if bm2f[j] >= 11:
                    match_dict[m1] = bm2v[j]

        if len(match_dict) == 0:
            #print("There are no matches between sensors", self.sn, "and", s2.sn)
            return


        # get the unique row/col ids of the beacons that appear in both scanner ranges
        # These are relative beacon ids - based on matrix col/row
        # translate to actual beacon ids
        s1bm = self.getBeaconIdsFromIndex(list(match_dict.keys()))
        s2bm = s2.getBeaconIdsFromIndex(list(match_dict.values()))

        if len(s1bm) < 12:
            print("Not enough for a good fix, moving on")
            return

        print("Found 12 common beacons.")
        print("Sensor", self.sn, "location is", self.location)
        print("Sensor", s2.sn, "location is", s2.location)

        #print(s1bm)
        #print(s2bm)

        #print("\nSensor", self.sn, "beacons:", s1bm, len(s1bm))
        gxd, gyd, gzd = self.getXYZDistributions(s1bm)
        #print("Good distributions","\n", gxd, "\n", gyd,"\n", gzd)

        #print("\nSensor", s2.sn, "beacons:", s2bm, len(s2bm))
        axd, ayd, azd = s2.getXYZDistributions(s2bm)
        #print("Alternate distributions","\n", axd,"\n", ayd,"\n", azd)

        rot_count = 0
        while (len(gxd) != len(axd) or len(gyd) != len(ayd) or len(gzd) != len(azd) or
                not all(gxd == axd) or not all(gyd == ayd) or not all(gzd == azd)):
            s2.rollAxes()
            axd, ayd, azd = s2.getXYZDistributions(s2bm)
            #print("Alternate distributions","\n", axd,"\n", ayd,"\n", azd)
            rot_count += 1
            if rot_count > 23:
                exit("BAD ROTATION")

        # get coords of matching beacons (first in list)
        mbc1 = self.getBeaconCoords(s1bm[0])
        mbc2 = s2.getBeaconCoords(s2bm[0])

        #print("Selected beacon locations to determine offset")
        #print(mbc1)
        #print(mbc2)

        # then get the diff and reset s2 coordinate system
        # NOTE that mbc1 uses UCS, from origin [0,0,0]
        # not coordinates relative to sensor self
        mbcdiff = mbc1 - mbc2

        print("Sensor", self.sn, "location is", self.location)
        print("Sensor", s2.sn, "location is", s2.location)
        print("SETTING LOCATION OF", s2.sn, "RELATIVE TO", self.sn, "offset by", mbcdiff)

        # the difference between MBC1 and MBC2 is the shift of the sensors!
        # But as S1 (MBC1) is always in UCS, this shift relative to UCS as well
        s2.location = mbcdiff
        s2.shiftAllBeaconLocationsToUCS()
        s2.updateBeaconIdsTo(self)
        s2.calcBeaconDistancesApart()
        s2.setUCS()

        # sanity check - no other sensor should be at [0,0,0]
        if s2.sn != 0 and all(s2.location == [0,0,0]):
            exit("BAD SENSOR LOCATION")

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

# check each scanner for a match with every other scanner
# can only match to those that are tied to Universal Coordinates System (UCS)
# only sensor id 0 starts as part of UCS and others progressively join
# and reset their beacon coordinates to UCS progressively
def searchForMatch():
    for s1 in so:
        # s1 must already be on UCS
        if s1.ucs:
            for s2 in so:
                if s2.ucs:
                    continue
                # go through all possible scanners that aren't s1
                if s1 != s2:
                    # see which beacon distances s1 has with s2 they have in common
                    s1.findDistMatches(s2)

def getUniqueBeacons():
    # count all the IDS
    ubd = {} # unique beacon dict
    for s in so:
        for bid, xyz in s.beacons.items():
            ubd[bid] = xyz
    return ubd

# the main driver loop
# keeps going until nothing changes for a full matrix check
last_beacon_count = None
beacon_count = None
while not all([s.ucs for s in so]) or last_beacon_count != beacon_count:
    last_beacon_count = len(getUniqueBeacons())
    searchForMatch()
    beacon_count = len(getUniqueBeacons())
    print("Last beacon count", last_beacon_count)
    print("Beacon count", beacon_count)

# get all beacon XYZ and then reduce for duplicate coordinates
bxyz = []
for s in so:
    for bid, xyz in s.beacons.items():
        if str(xyz) not in bxyz:
            bxyz.append(str(xyz))

### Part 1
print("=========== PART 1 ===============")
print("Part 1 answer", len(bxyz))
# guessed 580 - too high
# guessed 472 - too high
# guessed 448 - too high
# guessed 382 - ?? accounting for dupes - perhaps duplicates are more than *2?

### Part 2 - get all the distances between the sensors
print("=========== PART 2 ===============")
max_distance = None
for s1 in so:
    for s2 in so:
        if s1.sn == s2.sn:
            continue

        dist = np.array(s1.location, dtype=int) - np.array(s2.location, dtype=int)
        mdist = sum([abs(v) for v in dist])
        if max_distance is None or mdist > max_distance:
            #print(s1.sn, s2.sn, mdist)
            max_distance = mdist

print("Part 2 answer", max_distance)
