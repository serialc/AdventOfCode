#from math import prod
#import numpy as np
#import re

input_file = 'input0'
input_file = 'input'

class Hand:
    def __init__(self, handstr, bidstr, partone):

        self.cards = []
        self.codeCards(list(handstr), partone)
        self.bid = int(bidstr)
        self.kind = None
        self.determineType()

        # adjust kind value if part two
        if not partone:
            self.adjustKind()

    def __repr__(self):
        return "".join([str(x).split('x')[1] for x in self.cards]) + ':' + str(self.bid) + "-" + str(self.kind)

    def adjustKind(self):
        # do nothing if five of a kind
        if self.kind == 1:
            return

        # count number of jacks (given a value of 0x1) in parttwo
        jackcount = sum([c == hex(1) for c in self.cards])

        if jackcount == 1:
            # high card to pair
            if self.kind == 7:
                self.kind -= 1
                return
            # pair to threes, two-pair to fh, threes to fours, -2
            if self.kind > 3:
                self.kind -= 2
                return
            # fh not possible
            # 4 of a kind go up 1
            if self.kind == 2:
                self.kind -= 1
                return

        # either we have one pair, two pair, or full house
        if jackcount == 2:
            if self.kind == 5:
                # two pairs goes to fours, -3
                self.kind -= 3
            else:
                # go up by two (either pair to threes, fh to fives)
                self.kind -= 2
            return

        # either we have threes or fh
        if jackcount == 3:
            # go up by two (either threes to fours, fh to fives)
            self.kind -= 2
            return

        # fours
        if jackcount == 4:
            # goes to fives
            self.kind -= 1
            return

    def codeCards(self, cards, partone):
        for c in cards:
            if c.isdigit():
                self.cards.append(hex(int(c)))
            else:
                if c == 'T':
                    self.cards.append(hex(10))
                if c == 'J':
                    if partone:
                        self.cards.append(hex(11))
                    else:
                        self.cards.append(hex(1))
                if c == 'Q':
                    self.cards.append(hex(12))
                if c == 'K':
                    self.cards.append(hex(13))
                if c == 'A':
                    self.cards.append(hex(14))

    def determineType(self):

        # get card frequencies
        cfreq = dict()
        for c in self.cards:
            if c in cfreq:
                cfreq[c] += 1
            else:
                cfreq[c] = 1

        # now determine hand type based on frequencies
        # five of a kind
        if len(cfreq) == 1:
            self.kind = 1
            return

        # four of a kind or full-house
        if len(cfreq) == 2:
            if (cfreq[self.cards[0]] == 1 or
                cfreq[self.cards[0]] == 4):
                self.kind = 2
            else:
                self.kind = 3
            return

        # three of a kind, two pair
        if len(cfreq) == 3:
            if (cfreq[self.cards[0]] == 3 or
                cfreq[self.cards[1]] == 3 or
                cfreq[self.cards[2]] == 3):
                self.kind = 4
            else:
                self.kind = 5
            return

        # one pair
        if len(cfreq) == 4:
            self.kind = 6
            return

        # high card - all different
        if len(cfreq) == 5:
            self.kind = 7
            return

        exit("Hand->determineType failed to classify hand!")


    def getCards(self):
        return self.cards

    def getKind(self):
        return self.kind

    def getBid(self):
        return self.bid

    def isWinner(self, other):

        # lower number kind is 'winner'
        if self.kind < other.getKind():
            return True

        if self.kind > other.getKind():
            return False

        # higher number card is 'winner'
        # They are equal, go to card by card comparison
        other_cards = other.getCards()
        for i in range(len(self.cards)):

            if self.cards[i] > other_cards[i]:
                return True

            if self.cards[i] < other_cards[i]:
                return False

            # didn't find any difference, go to next card

        return false


hands = []
with open(input_file, 'r') as fh:
    for l in fh:
        l = l.strip('\n')
        hand, bid = l.split()
        # boolean handles part 2
        hands.append(Hand(hand, bid, True))

# sanity check
#print(hands)

# repeat until sorted
while True:
    changes = 0
    # go through list
    for i in range(len(hands)-1):
        # test neighbours, swap if needed
        # winning hands go down
        if hands[i].isWinner(hands[i+1]):
            temp = hands[i+1]
            hands[i+1] = hands[i]
            hands[i] = temp
            changes += 1

    if changes == 0:
        break

winnings = 0
hid = 1
for h in hands:
    winnings += h.getBid() * hid
    hid += 1

print("#### Part 1 ####")
print("Answer is:", winnings)

#### PART 2 ####
print("============ Part 2 start ================")

hands = []
with open(input_file, 'r') as fh:
    for l in fh:
        l = l.strip('\n')
        hand, bid = l.split()
        # boolean handles part 2
        hands.append(Hand(hand, bid, False))

# repeat until sorted
while True:
    changes = 0
    # go through list
    for i in range(len(hands)-1):
        # test neighbours, swap if needed
        # winning hands go down
        if hands[i].isWinner(hands[i+1]):
            temp = hands[i+1]
            hands[i+1] = hands[i]
            hands[i] = temp
            changes += 1

    if changes == 0:
        break

winnings = 0
hid = 1
for h in hands:
    winnings += h.getBid() * hid
    hid += 1

print("#### Part 2 ####")
print("Answer is:", winnings)
# not 253299703 - too low, had bad 'kind' shift for one card
