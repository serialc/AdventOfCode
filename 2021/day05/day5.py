import numpy as np

# get coords in readable
vcoords = []
# assume 0,0 is min
with open('input', 'r') as fh:
    for line in fh:
        line = line.strip()
        o,d = line.split(' -> ')
        x1,y1 = o.split(',')
        x2,y2 = d.split(',')
        vcoords.append([x1,y1,x2,y2])

vc = np.array(vcoords, dtype=int)
# these are indices values, need to inc by one
xmax = np.max(np.max(vc[:,[0,2]], 0)) + 1
ymax = np.max(np.max(vc[:,[1,3]], 0)) + 1

# create empty seafloor of correct size
esf = np.zeros(xmax*ymax, dtype=int).reshape([xmax, ymax])

#### Part 1 ####
def mapSeafloor(sf, mode='diag'):
    for vl in vc:
        # skip diagonals
        if mode == 'notdiag': 
            if vl[0] != vl[2] and vl[1] != vl[3]:
                continue

        xshift = 1
        if vl[2] < vl[0]:
            xshift = -1
        yshift = 1
        if vl[3] < vl[1]:
            yshift = -1
        
        xc = [x for x in range(vl[0], vl[2]+xshift, xshift)]
        yc = [y for y in range(vl[1], vl[3]+yshift, yshift)]

        for i in range(max(len(xc),len(yc))):
            yi = yc[i%len(yc)]
            xi = xc[i%len(xc)]
            # x/y backwards in indexing
            sf[yi, xi] = sf[yi, xi] + 1 

    return sf


p1sf = mapSeafloor(esf.copy())
print("Part 1 answer is", np.sum(p1sf) >= 2)
print(esf)

#### Part 2 ####
p2sf = mapSeafloor(esf.copy())
print("Part 2 answer is", np.sum(p2sf) >= 2)
print("Generated image")

#### Bonus ####
from PIL import Image
im = Image.new('RGB', p2sf.shape)
sfmax = np.max(p2sf)

pixellist = []
for row in p2sf:
    for c in row:
        if c == 0:
            #pixellist.append((0,50,148))
            pixellist.append((255,255,255))
        else:
            pval = int(c/sfmax*255)
            pixellist.append((255,255 - pval, 255 - pval))
im.putdata(pixellist)
im.save('seafloor.png')
