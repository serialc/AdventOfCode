#from math import prod
import numpy as np
import re

input_file = 'input0'
input_file = 'input'

cards = {}
acs = 0
with open(input_file, 'r') as fh:
    for l in fh:
        l = l.strip('\n')

        # parse the data
        cardid, numsets = l.split(': ')
        cardid = int(cardid.split()[1])
        win, mynum = numsets.split(' | ')

        # split and convert to int
        win = [int(x) for x in win.split()]
        mynum = [int(x) for x in mynum.split()]

        # count points for card / presence of mynumbers in winning set
        cardsum = sum([x in win for x in mynum])
        # it's a power of 2 (-1)
        if cardsum > 0:
            acs += pow(2, cardsum - 1)

        # save
        cards[cardid] = [win, mynum, cardsum]

print(cards)
print("#### Part 1 ####")
print("Answer is:", acs)

#### PART 2 ####
print("============ Part 2 start ================")

freq = np.ones(len(cards), int)

# go through each card
for cid, card in cards.items():
    # if the card has any points
    if card[2] > 0:
        # subset the next n cards, where n is the number of points this card has
        # then add the frequency of this card to those n cards
        # note the indices are off (card 1 -> freq[0])
        freq[cid:cid+card[2]] += freq[cid-1]

print(freq)
print("#### Part 2 ####")
print("Answer is:", freq.sum())
