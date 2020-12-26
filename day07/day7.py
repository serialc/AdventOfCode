#import numpy as np
import re

bdict = {}
bndict = {}
with open('input.txt', 'r') as fh:
    for line in fh:

        line = line.rstrip()
        line = line.rstrip('.')
        parent, subbags = line.split(" bags contain ")

        if subbags == 'no other bags':
            bdict[parent] = []
            bndict[parent] = []
            continue

        subbags = subbags.split(', ')
        for bag in subbags:
            bag = bag.split(" bag")[0]
            count, bag = re.search('^(\d+) (.+)$', bag).groups()

            if parent in bdict:
                bdict[parent].append(bag)
                bndict[parent].append({bag: int(count)})
            else:
                bdict[parent] = [bag]
                bndict[parent] = [{bag: int(count)}]

# Answer Part 1

def contains_shiny_gold(this_bag):
    if this_bag == 'shiny gold':
        #print("Found it!")
        return True
    if len(bdict[this_bag]) == 0:
        #print("Nope!")
        return False
    for bag in bdict[this_bag]:
        #print("- within " + bag)
        if contains_shiny_gold(bag):
            return True

    # failed to find it
    return False


# now see if each bag can lead to a 'shiny gold'
bsum = 0
for bag in bdict:
    # skip if this bag is shiny gold - we only want those inside another bag
    if bag == 'shiny gold':
        continue
    
    #print("Looking in " + bag)
    if contains_shiny_gold(bag):
        bsum += 1

# Part 1 answer
print('Part 1 - Bag-colours possible containing a shiny gold bag: ' + str(bsum))


# Answer Part 2

# Part 2 answer
def bags_within(this_bag):
    bag_sum = 1
    if len(bndict[this_bag]) == 0:
        return 1

    for bag in bndict[this_bag]:
        bag, count = next(iter( bag.items() ))
        #print(bag, count)
        bag_sum += bags_within(bag) * count
    return bag_sum

#print(bndict)
bsum = bags_within('shiny gold') - 1 # don't count the shiny gold bag

print("Part 2 - Number of bags in a gold bag: " + str(bsum))
