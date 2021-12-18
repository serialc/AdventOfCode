import numpy as np

input_file = 'pre_test_input'
input_file = 'test_input'
input_file = 'test_input1'
#input_file = 'input'

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

        self.depth = depth
        if isinstance(self.left, int):
            self.ldindex = digit_index
            digit_index += 1
        else:
            self.left.mapDepthAndDigits(depth+1)

        if isinstance(self.right, int):
            self.rdindex = digit_index
            digit_index += 1
        else:
            self.right.mapDepthAndDigits(depth+1)

    def explodeCheck(self, notify=False):
        global movements
        global action_happened

        if notify:
            print("EXPLODE CHECKING")

        # if we've already had an explosion just return False
        # we'll get it the next iteration
        if action_happened:
            return True

        explosions_count = 0

        #print("ExplodeCheck",self.getStr())

        # if the left node is a pair and too deep
        if not isinstance(self.left, int):
            if self.left.depth == 4:
                print("Exploded",self.left.getStr())
                action_happened = True
                # can move the exploded right here
                print(self.getStr())
                self.right += self.left.right
                # add to list of things to do
                movements[self.left.ldindex-1] = self.left.left
                self.left = 0
                return True
            elif self.left.explodeCheck():
                    explosions_count += 1

        # if the right node is a pair and too deep
        if not isinstance(self.right, int):
            if self.right.depth == 4:
                print("Exploded",self.right.getStr())
                action_happened = True
                # can move the exploded left here
                self.left += self.right.left
                # add to list of things to do
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

        # if we've already had a split just return False
        # we'll get it the next iteration
        if action_happened:
            return True

        split_count = 0

        if isinstance(self.left, int):
            if self.left > 9:
                node = Node()
                node.fromPair(int(self.left/2), int(self.left/2+0.5))
                self.left = node
                split_count += 1
                action_happened = True
        elif self.left.splitCheck():
            split_count += 1

        if isinstance(self.right, int):
            if self.right > 9:
                node = Node()
                node.fromPair(int(self.right/2), int(self.right/2+0.5))
                self.right = node
                split_count += 1
                action_happened = True
        elif self.right.splitCheck():
            split_count += 1

        if split_count > 0:
            return True
        else:
            return False

    def movementCheck(self):
        global movements

        if len(movements) > 0:
            print("There are movements pending", movements)
            self.moveValues()

            # reset to remove out of index values
            movements = dict()

    def moveValues(self):
        global movements

        # walk the tree and see if we can find the id in the movements dict
        if isinstance(self.left, int):
            #print("DEBUG L- this value", self.left, "and id", self.ldindex,"looking for", movements)
            if self.ldindex in movements:
                self.left += movements[self.ldindex]
                del movements[self.ldindex]
            return

        if isinstance(self.right, int):
            #print("DEBUG R- this value", self.left, "and id", self.rdindex,"looking for", movements)
            if self.rdindex in movements:
                self.right += movements[self.rdindex]
                del movements[self.rdindex]
            return


        self.left.moveValues()
        self.right.moveValues()
    
### Read input data
tree = None
movements = dict()
digit_index = 0
action_happened = False

with open(input_file, 'r', encoding='utf-8-sig') as fh:
    last_node = None
    for line in fh:
        line = line.strip()

        # explosion testing
        #line = "[[[[[9,8],1],2],3],4]"
        #line = "[7,[6,[5,[4,[3,2]]]]]"
        #line = "[[6,[5,[4,[3,2]]]],1]"
        #line = "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"

        print("Next nested input line", line)

        node = Node()
        node.fromString(line)
        print("Built line into node", node.getStr())

        # merge node to previous node tree = [tree, node]
        if last_node is None:
            last_node = node
            continue

        tree = Node()
        tree.fromPair(last_node, node)

        tree.mapDepthAndDigits()
        print("\nJoined tree", tree.getStr())

        while(tree.explodeCheck(True) or tree.splitCheck(True)):
            # clean up before checking again
            print("Explosion or Split happened. Clean up and do next iteration")
            tree.movementCheck()
            tree.mapDepthAndDigits()
            action_happened = False

            # show state
            print("After explode or split", tree.getStr(), "\n")

        print("Result", tree.getStr())
        print("Process next row\n\n")
        last_node = tree


print("Final result", tree.getStr())
### Part 1
print("=========== PART 1 ===============")
print("Part 1 answer", 999)

### Part 2
print("=========== PART 2 ===============")
print("Part 2 answer", 999)
