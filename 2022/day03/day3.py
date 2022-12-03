import numpy as np

def getVal (char):
    # A is 65 => needs to be 27 (so -38)
    # a is 97 => needs to be 1 (so -96)
    print(char)
    if ord(char) >= 97:
        return ord(char) - 96
    else:
        return ord(char) - 38

prisum = 0
with open('input.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:
    for line in fh:
        line = line.strip('\n')

        # split into two parts
        p1 = line[0:int(len(line)/2)]
        p2 = line[int(len(line)/2):]

        # create a dict and put each of the first parts (once)
        d = {}
        for x in p1:
            d[x]=True

        # go through the second part, if it's in the above dict - that's our letter
        dbl = None
        for x in p2:
            if x in d:
                dbl = x
                break

        # look up it's value
        prisum += getVal(dbl)

# Part 1
print("#### Part 1 ####")
print("Score " + str(prisum))

################################ PART 2 ######################


grpsum = 0
with open('input.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:
    grp_elfnum = 0
    d = {}
    for line in fh:
        line = line.strip('\n')

        # for first elf just populate a dict
        if grp_elfnum == 0:
            d = {}
            for x in line:
                d[x]=True
            
        # for the 2nd/3rd elves look through the above dict and
        # see if elf 2/3 has the item - if not remove item from dict
        if grp_elfnum == 1 or grp_elfnum == 2:
            dcopy = d.copy()
            for x in d.keys():
                if x not in line:
                    dcopy.pop(x)
            d = dcopy
        
        # there should only be one item left in dict - get it's value and add to our sum
        if grp_elfnum == 2:
            ltr = list(d.keys())[0]
            ltrval = getVal(ltr)
            print(ltr + ':' + str(ltrval))
            grpsum += ltrval


        # determine which elf we're looking at
        grp_elfnum = (grp_elfnum + 1)%3

# Part 2
print("#### Part 2 ####")
print("Score " + str(grpsum))
