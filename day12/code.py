# day 11
import math

input_file = 'input_test.txt'
input_file = 'input.txt'

locx = 0
locy = 0
heading = 0
headings = ['E', 'S', 'W', 'N']

with open(input_file, 'r') as fh:
    for line in fh:
        line = line.rstrip()

        cmd = line[0:1]
        val = int(line[1:])

        if cmd == 'F':
            # figure out what direction we are heading
            # adjust cmd
            cmd = headings[heading % 4]
        if cmd == 'N':
            locy -= val
        if cmd == 'S':
            locy += val
        if cmd == 'E':
            locx += val
        if cmd == 'W':
            locx -= val
        if cmd == 'R':
            heading += int(val/90)
        if cmd == 'L':
            heading -= int(val/90)

        #print(line + ' ' + str(locx) + ',' + str(locy) + ' ' + headings[heading%4])

print("Part 1 - Manhattan distance from origin is " + str(abs(locx) + abs(locy)))

# Part 2 - waypoint

# destination relative to the ship
wpx = 10
wpy = -1
# coordinates of the ship
locx = 0
locy = 0

with open(input_file, 'r') as fh:
    for line in fh:
        line = line.rstrip()

        cmd = line[0:1]
        val = int(line[1:])

        if cmd == 'F':
            # figure out what direction we are heading
            # adjust cmd
            locx += val * wpx
            locy += val * wpy
        if cmd == 'N':
            wpy -= val
        if cmd == 'S':
            wpy += val
        if cmd == 'E':
            wpx += val
        if cmd == 'W':
            wpx -= val
        if cmd == 'R':
            # careful, we change the source 
            wpx,wpy = [
                round(math.cos(math.radians(val)) * wpx - math.sin(math.radians(val)) * wpy),\
                round(math.sin(math.radians(val)) * wpx + math.cos(math.radians(val)) * wpy)
                ]
        if cmd == 'L':
            # careful, we change the source 
            wpx,wpy = [
                round(math.cos(math.radians(-val)) * wpx - math.sin(math.radians(-val)) * wpy),\
                round(math.sin(math.radians(-val)) * wpx + math.cos(math.radians(-val)) * wpy)
                ]

        #print(line + (' '*(6-len(line))) + str(locx) + ',' + str(locy), end='')
        #print(' ' + str(wpx) + ',' + str(wpy))

print("Part 2 - Manhattan distance from origin is " + str(abs(locx) + abs(locy)))
