import numpy as np

#input_file = 'pre_test_input'
#input_file = 'test_input'
#input_file = 'test_input0'
#input_file = 'test_input1'
#input_file = 'test_input2'

input_file = 'test_input_larger'
input_file = 'test_input_homework'

#input_file = 'test_magnitude'

input_file = 'input'

class Node:

    left = None
    right = None
    depth = None
    # left/right digit indices
    ldindex = None
    rdindex = None

    def __init__(self):
        pass

    def fromString(self, s):

        # Left part
        if s[1].isdigit():
            self.left = int(s[1])
            divi = 2
        else:
            # not a digit, get sub pair limits
            bstack = 1
            srch = 2
            while bstack > 0:
                if s[srch] == '[':
                    bstack += 1
                if s[srch] == ']':
                    bstack -= 1
                srch += 1
                
            divi = srch
            self.left = Node()
            self.left.fromString(s[1:srch])

        # Right part
        if s[-2].isdigit():
            self.right = int(s[-2])
        else:
            self.right = Node()
            self.right.fromString(s[divi + 1:-1])

    def fromPair(self, left, right):
        self.left  = left
        self.right = right

    def getStr(self):
        resp = "["

        if isinstance(self.left, int):
            resp += str(self.left)
        else:
            resp += self.left.getStr()

        resp += ","

        if isinstance(self.right, int):
            resp += str(self.right)
        else:
            resp += self.right.getStr()

        resp += "]"

        return resp

    def mapDepthAndDigits(self, depth=0):
        global digit_index
        global digit_index

        depth_debug = False

        if depth == 0:
            digit_index = 0
            if depth_debug:
                print("Depth of digits: ", end="")

        self.depth = depth
        if isinstance(self.left, int):
            if depth_debug:
                print(depth, end='')
                #print(digit_index, end='')
                pass
            self.ldindex = digit_index
            digit_index += 1
        else:
            self.left.mapDepthAndDigits(depth+1)

        if isinstance(self.right, int):
            if depth_debug:
                print(depth, end='')
                #print(digit_index, end='')
                pass
            self.rdindex = digit_index
            digit_index += 1
        else:
            self.right.mapDepthAndDigits(depth+1)

        if depth == 0:
            if depth_debug:
                print()
                pass

    def explodeCheck(self, notify=False):
        global movements
        global action_happened

        if notify:
            print("EXPLODE CHECKING")
            pass

        # if we've already had an explosion just return False
        # we'll get it the next iteration
        if action_happened:
            return True

        explosions_count = 0

        #print("Explode Check at depth", self.depth, self.getStr())

        # if the left node is a pair and too deep
        if not isinstance(self.left, int):
            if self.left.depth >= 4:
                print("Exploded Left child at depth", self.left.depth, "containing",self.left.getStr())
                action_happened = True
                # add to list of things to do
                movements[self.left.ldindex-1] = self.left.left
                movements[self.left.rdindex+1] = self.left.right
                self.left = 0
                return True
            elif self.left.explodeCheck():
                    explosions_count += 1

        # if the right node is a pair and too deep
        if not isinstance(self.right, int):
            if self.right.depth == 4:
                print("Exploded Right child at depth", self.right.depth, "containing", self.right.getStr())
                action_happened = True
                # add to list of things to do
                movements[self.right.ldindex-1] = self.right.left
                movements[self.right.rdindex+1] = self.right.right
                self.right = 0
                return True
            elif self.right.explodeCheck():
                    explosions_count += 1

        if explosions_count > 0:
            return True
        else:
            return False

    def splitCheck(self, notify=False):
        global action_happened

        if notify:
            print("SPLIT CHECKING")
            pass

        # if we've already had a split just return False
        # we'll get it the next iteration
        if action_happened:
            return True

        if isinstance(self.left, int):
            if self.left > 9:
                node = Node()
                node.fromPair(int(self.left/2), int(self.left/2+0.5))
                self.left = node
                action_happened = True
                return True
        else:
            if self.left.splitCheck():
                return True

        if isinstance(self.right, int):
            if self.right > 9:
                node = Node()
                node.fromPair(int(self.right/2), int(self.right/2+0.5))
                self.right = node
                action_happened = True
                return True
        else:
            if self.right.splitCheck():
                return True

        return False

    def movementCheck(self):
        global movements

        if len(movements) > 0:
            #print("There are movements pending", movements)
            self.moveValues()

            # reset to remove out of index values
            movements = dict()


    def moveValues(self):
        global movements

        if len(movements) == 0:
            return

        # walk the tree and see if we can find the id in the movements dict
        if isinstance(self.left, int):
            #print("DEBUG L- this value", self.left, "and id", self.ldindex,"looking for", movements)
            if self.ldindex in movements:
                self.left += movements[self.ldindex]
                del movements[self.ldindex]
        else:
            self.left.moveValues()

        if isinstance(self.right, int):
            #print("DEBUG R- this value", self.left, "and id", self.rdindex,"looking for", movements)
            if self.rdindex in movements:
                self.right += movements[self.rdindex]
                del movements[self.rdindex]
        else:
            self.right.moveValues()

    def getMagnitude(self):
        mag = 0

        #print(self.getStr())
        if isinstance(self.left, int):
            mag += self.left * 3
        else:
            mag += self.left.getMagnitude() * 3

        if isinstance(self.right, int):
            mag += self.right * 2
        else:
            mag += self.right.getMagnitude() * 2

        #print("Magnitude", mag)
        return mag 

    
### Read input data
tree = None
movements = dict()
digit_index = 0
action_happened = False

snums_list = []
with open(input_file, 'r', encoding='utf-8-sig') as fh:
    for line in fh:
        line = line.strip()
        snums_list.append(line)


def processSnailFishNumbers(sfnl):
    global tree
    global movements
    global digit_index
    global action_happened

    tree = None
    movements = dict()
    digit_index = 0
    action_happened = False

    last_node = None
    jcount = 0

    for line in sfnl:
        node = Node()
        node.fromString(line)
        #print("Next nested input line", line)
        #print("Built line into node", node.getStr())

        # merge node to previous node tree = [tree, node]
        if last_node is None:
            last_node = node
            continue

        tree = Node()
        tree.fromPair(last_node, node)

        tree.mapDepthAndDigits()
        #print("\nJoined tree", tree.getStr())

        cycle = 0
        while(tree.explodeCheck(True) or tree.splitCheck(True)):
            # clean up before checking again
            #print("\nCYCLE", cycle, "- Explosion or Split happened. Starting clean up before next iteration")
            tree.movementCheck()
            tree.mapDepthAndDigits()
            action_happened = False

            # show state
            #print("After explode or split", tree.getStr())
            cycle += 1

        #print("Result", tree.getStr())
        #print("Process next row")
        last_node = tree

        jcount += 1

        if jcount == 2:
            #exit("EXIT")
            pass

print(snums_list)
processSnailFishNumbers(snums_list)

print("Final result", tree.getStr())
### Part 1
print("=========== PART 1 ===============")
print("Part 1 answer", tree.getMagnitude())

### Part 2
print("=========== PART 2 ===============")

max_pair_mag = 0
winning_lines = None
for line1 in snums_list:
    for line2 in snums_list:
        if line1 == line2:
            continue
        else:
            print([line1, line2])
            processSnailFishNumbers([line1, line2])
            mag = tree.getMagnitude()
            if mag > max_pair_mag:
                winning_lines = [line1, line2]
                max_pair_mag = mag


print(winning_lines)
print("Part 2 answer", max_pair_mag)
