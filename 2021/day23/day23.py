import numpy as np

input_file = 'test_input'
#input_file = 'input'

def matPrint(mat):
    h,w = mat.shape
    for y in range(h):
        for x in range(w):
            print(mat[y,x], end='')
        print()
    print()

cave = []
with open(input_file, 'r') as fh:
    w = None
    h = 0
    for line in fh:
        line = line.strip('\n')
        if w == None:
            w = len(line)
        while len(line) < w:
            line += ' '
        cave.append(list(line))
        h += 1
cave = np.array(cave).reshape((h,w))

def getPossibleMoves(
matPrint(cave)

# movement energy requirements
mnrg = {'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000}

# Other rules
# - can't stop at room exits
# - only stop once outside room
# - only go to room as final destination
# - really, each snail only has two moves max (can move directly from room to room through)

##### PART 1 #####
print("Part 1")
# Tried 10421 - too high - Math error!
# Answer is 10321

##### PART 2 #####
print("Part 2")
