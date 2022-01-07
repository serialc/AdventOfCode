import numpy as np

input_file = 'test_input'
input_file = 'input'

def matPrint(mat):
    h,w = mat.shape
    for y in range(h):
        for x in range(w):
            print(mat[y,x], end='')
        print()
    print()

cave = []
# '#' walls
# '.' space to move through at cost
# '*' or letter are places one can rest

# snails only move into their cave if it's either empty or has one of their types there
# each snail gets two moves maximum, of any distance, one out of cave, then in a cave

class Snail:
    def __init__(self, stype, pos):
        self.type = stype
        self.pos = pos

    def __str__(self):
        return(self.type + "@" + str(self.pos))

    def getPossibleMoves(self, cave):
        # find all accessible locations of '_' in cave
        pass

snails = []
ezones = dict()
with open(input_file, 'r') as fh:
    rownum = 0
    for line in fh:
        line = line.strip('\n')
        row = []
        colnum = -1
        ezstr = list('DCBA')

        for c in list(line):
            colnum += 1
            if c == '#':
                row.append('#')
                continue
            if c == '*':
                row.append('_')
                continue
            if c == '.': 
                row.append('.')
                continue
            
            # rest are snails
            # spots are occupied
            row.append('o')
            pos = [rownum, colnum]
            snails.append(Snail(c, pos))

            # need to create exclusion zones based on snail types
            if rownum > 1:
                ezones[str(pos)] = ezstr.pop()

        rownum += 1

        cave.append(row)
cave = np.array(cave)

matPrint(cave)
[print(s) for s in snails]
print(ezones)


# movement energy requirements
mnrg = {'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000}

# Other rules
# - can't stop at room exits
# - only stop once outside room
# - only go to room as final destination
# - each snail has two moves max (can move directly from room to room through)

##### PART 1 #####
print("Part 1")
# Tried 10421 - too high - Math error!
# Answer is 10321

##### PART 2 #####
print("Part 2")
