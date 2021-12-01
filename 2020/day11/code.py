# day 11

input_file = 'input_test.txt'
input_file = 'input.txt'
debug = False

blankseatmap = []
with open(input_file, 'r') as fh:
    for line in fh:
        line = line.rstrip()
        blankseatmap.append([c for c in line])

def neighbours(y,x):
    mx = len(seatmap[0])
    my = len(seatmap)

    ncount = 0
    # 8 1 2
    # 7 X 3
    # 6 5 4

    # Note the tests are offset from edge here
    # Tests are one over from x/y
    # in vneighbours the test is on the value of interest
    if y > 0 and seatmap[y-1][x] == '#':
        ncount += 1
    if y > 0 and x < (mx - 1) and seatmap[y-1][x+1] == '#':
        ncount += 1
    if x < (mx - 1) and seatmap[y][x+1] == '#':
        ncount += 1
    if x < (mx - 1) and y < (my - 1) and seatmap[y+1][x+1] == '#':
        ncount += 1
    if y < (my - 1) and seatmap[y+1][x] == '#':
        ncount += 1
    if x > 0 and y < (my - 1) and seatmap[y+1][x-1] == '#':
        ncount += 1
    if x > 0 and seatmap[y][x-1] == '#':
        ncount += 1
    if x > 0 and y > 0 and seatmap[y-1][x-1] == '#':
        ncount += 1

    return ncount

def vneighbours(y,x):
    mx = len(seatmap[0])
    my = len(seatmap)

    debug = []
    ncount = 0
    # 8 1 2
    # 7 X 3
    # 6 5 4

    # Here we shift the value, then test THAT value, different from neighbours

    # up
    ty = y - 1
    tx = x
    while ty >= 0:
        if seatmap[ty][tx] == '#':
            ncount += 1
            debug.append(1)
            break
        if seatmap[ty][tx] == 'L':
            break
        ty -= 1

    # up-right
    ty = y - 1
    tx = x + 1
    while ty >= 0 and tx < mx:
        if seatmap[ty][tx] == '#':
            ncount += 1
            debug.append(2)
            break
        if seatmap[ty][tx] == 'L':
            break
        ty -= 1
        tx += 1

    # right
    tx = x + 1
    ty = y
    while tx < mx:
        if seatmap[ty][tx] == '#':
            ncount += 1
            debug.append(3)
            break
        if seatmap[ty][tx] == 'L':
            break
        tx += 1

    # right-down
    tx = x + 1
    ty = y + 1
    while tx < mx and ty < my:
        if seatmap[ty][tx] == '#':
            ncount += 1
            debug.append(4)
            break
        if seatmap[ty][tx] == 'L':
            break
        tx += 1
        ty += 1

    # down
    ty = y + 1
    tx = x
    while ty < my:
        if seatmap[ty][tx] == '#':
            ncount += 1
            debug.append(5)
            break
        if seatmap[ty][tx] == 'L':
            break
        ty += 1

    # down-left
    tx = x - 1
    ty = y + 1
    while tx >= 0 and ty < my:
        if seatmap[ty][tx] == '#':
            ncount += 1
            debug.append(6)
            break
        if seatmap[ty][tx] == 'L':
            break
        tx -= 1
        ty += 1

    # left
    tx = x - 1
    ty = y
    while tx >= 0:
        if seatmap[ty][tx] == '#':
            ncount += 1
            debug.append(7)
            break
        if seatmap[ty][tx] == 'L':
            break
        tx -= 1

    # left-up
    tx = x - 1
    ty = y - 1
    while tx >= 0 and ty >= 0:
        if seatmap[ty][tx] == '#':
            ncount += 1
            debug.append(8)
            break
        if seatmap[ty][tx] == 'L':
            break
        tx -= 1
        ty -= 1

    #if x == 1 and y == 1:
        #print(debug)

    return ncount

def printseats():
    for y in range(len(seatmap)):
        if debug:
            for x in range(len(seatmap[0])):
                print(seatmap[y][x], end='')
        print('  ', end='')
        for x in range(len(seatmap[0])):
            print(nseatmap[y][x], end='')
        print('  ', end='')
        if debug:
            for x in range(len(vismap[0])):
                print(vismap[y][x], end='')
        print()

# Part 1 processing
seatmap = [row[:] for row in blankseatmap]
vismap  = [row[:] for row in blankseatmap]

iteration = 1
seated = 0
while True:
    # copy of object, not point to same object
    nseatmap = [row[:] for row in seatmap]

    for y in range(len(seatmap)):
        for x in range(len(seatmap[0])):
            if seatmap[y][x] == '.':
                continue

            n = neighbours(y,x)
            # for debugging
            vismap[y][x] = n

            # cellular automata rules
            if seatmap[y][x] == 'L' and n == 0:
                nseatmap[y][x] = '#'
            if n > 3:
                nseatmap[y][x] = 'L'
                vismap[y][x] = 'L'
            # otherwise stays the same

    #print("Iteration " + str(iteration))
    #printseats()

    if seatmap == nseatmap:
        print("No change - found the solution")
        break
    else:
        seatmap = nseatmap

    # count seated people
    seated = sum([sum([1 for item in row if item == '#']) for row in seatmap])
    print(str(seated) + '-', end='')

    if iteration > 100:
        print("Iteration limit reached, exiting")
        break

    iteration += 1

printseats()
print("Part 1 answer is: " + str(seated) + "\n\n")

# Part 2 work

seatmap = [row[:] for row in blankseatmap]
vismap  = [row[:] for row in blankseatmap]
iteration = 1
seated = 0
while True:
    # copy of object, not point to same object
    nseatmap = [row[:] for row in seatmap]

    for y in range(len(seatmap)):
        for x in range(len(seatmap[0])):
            if seatmap[y][x] == '.':
                continue

            n = vneighbours(y,x)
            # for debugging
            vismap[y][x] = n

            # cellular automata rules
            if seatmap[y][x] == 'L' and n == 0:
                nseatmap[y][x] = '#'
            if n > 4:
                nseatmap[y][x] = 'L'
                vismap[y][x] = 'L'
            # otherwise stays the same

    #print("Iteration " + str(iteration))
    #printseats()

    if seatmap == nseatmap:
        print("No change - found the solution")
        break
    else:
        seatmap = nseatmap

    # count seated people
    seated = sum([sum([1 for item in row if item == '#']) for row in seatmap])
    print(str(seated) + '-', end='')

    if iteration > 100:
        print("Iteration limit reached, exiting")
        break

    iteration += 1
printseats()
print("Part 2 answer is: " + str(seated))
