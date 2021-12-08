import numpy as np

inputf = 'first_input'
inputf = 'test_input'
inputf = 'input'

# segment ids
#  1111 
# 2    3
# 2    3
#  4444
# 5    6
# 5    6
#  7777

dig2segpos = {
        0: [1,2,3,5,6,7],
        1: [3,6],
        2: [1,3,4,5,7],
        3: [1,3,4,6,7],
        4: [2,3,4,6],
        5: [1,2,4,6,7],
        6: [1,2,4,5,6,7],
        7: [1,3,6],
        8: [1,2,3,4,5,6,7],
        9: [1,2,3,4,6,7]
        }

segnum_from_digit = {k:len(v) for k,v in dig2segpos.items()} 
# digit_from_segnum overwrites but we only use the good/easy parts
digit_from_segnum = {v:k for k,v in segnum_from_digit.items()} 

#print("segnum_from_digit", segnum_from_digit)
#print("digit_from_segnum", digit_from_segnum)

# 1,4,7,8
easy_seg_count = [2,4,3,7]

class Ssd:


    def __init__(self, ten_patterns):
        #re/set
        self.reset()

        # go through the ten patterns and decode
        for segcode in ten_patterns.split():
            # one digital pattern with multiple segments/letters
            self.addInfo(segcode)

        # figure out the left side and then the right (of the 7-segment display)
        self.processFiveSegmenters()
        self.clean()
        self.processTheSix()

    def reset(self):
        self.codes = {}
        self.poss = {x:[] for x in range(1,8)}
        self.notposs = {x:[] for x in range(1,8)}
        self.coded_segments = []

    def setSegmentIsNot(self, seg, letter):
        if letter in self.poss[seg]:
            self.poss[seg].remove(letter)
        if letter not in self.notposs[seg]:
            self.notposs[seg].append(letter)

    def setSegmentMayBe(self, seg, letter):
        if letter in self.notposs[seg]:
            # do not add to possible list
            return
        if letter not in self.poss[seg]:
            self.poss[seg].append(letter)

    def addEasyInfo(self, digit, segcode):
        # Populate the 7 segments with what they can or can't be
        for seg in self.poss.keys():
            # only look at the segments that this digit touches
            if seg in dig2segpos[digit]:

                # this segment has one of the characters from the segcode
                # add segment code letters to list of possible location segments
                for letter in list(segcode):
                    if letter not in self.poss[seg]:
                        # add to list of possible letters for this segment
                        self.setSegmentMayBe(seg, letter)

                # we also need to remove other letters present that are not part of segcode
                # and add them to the notposs list for these locations
                removal_list = []
                # don't change the item you're iterating through
                for letter in self.poss[seg]:
                    if letter not in segcode:
                        removal_list.append(letter)
                for letter in removal_list:
                    self.setSegmentIsNot(seg, letter)
            else:
                # this segment does not have any of the characters from the segcode
                # add segment code letters to list of not possible location segments
                for letter in list(segcode):
                    if letter not in self.notposs[seg]:
                        # add letter to banned for this segment list
                        self.notposs[seg].append(letter)
                    # see if the letter is present in possible list and remove if so
                    if letter in self.poss[seg]:
                        self.poss[seg].remove(letter)

    def addInfo(self, segcode):
        # save for later
        self.coded_segments.append(segcode)

        # use the easy ones to narrow it down
        segnum = len(segcode)
        if segnum in easy_seg_count:
            digit = digit_from_segnum[segnum]
            #print("\nSegment number ", segnum, " meaning digit ", digit)
            self.addEasyInfo(digit, segcode)

    def getLonelyLetters(self, letter_list):
        lcount = dict()
        # make a histogram
        for letter in list(letter_list):
            if letter in lcount:
                lcount[letter] += 1
            else:
                lcount[letter] = 1
        return [letter for letter, count in lcount.items() if count == 1]


    def processFiveSegmenters(self):
        #five_segment_digits = [d for d, slist in dig2segpos.items() if len(slist) == 5]
        five_segment_chars = [seg for seg in self.coded_segments if len(seg) == 5]
        key_letters = self.getLonelyLetters(list(''.join(five_segment_chars)))

        #print("\nFive segment key letters are", key_letters)

        # segments 2 and 5 must be either of these 
        for seg in [2,5]:
            # don't change the item you're iterating through
            removal_list = []
            for letter in self.poss[seg]:
                if letter not in key_letters:
                    removal_list.append(letter)
            # make changes
            for letter in removal_list:
                self.setSegmentIsNot(seg, letter)

    def processTheSix(self):
        # the six is the last key
        # it has only one segment that it shares with the one
        # the other 6-segment numbers, 9,0 share two with it

        six_segment_chars = [seg for seg in self.coded_segments if len(seg) == 6]
        for segcode in six_segment_chars:
            # count how many segments in common between 1 and 6,9,0
            segmatch = 0
            last_match_letter = ''
            for letter in list(segcode):
                if letter in self.poss[6]:
                    segmatch += 1
                    last_match_letter = letter
            if segmatch == 1:
                # this segcode is the in position 6!
                # and not in position 3
                self.setSegmentIsNot(3, last_match_letter)

                self.clean()
                self.createCodeTable()
                return

    def createCodeTable(self):
        for digit, segments in dig2segpos.items():
            segletters = [self.poss[seg][0] for seg in segments]
            digitcode = "".join(sorted(segletters))
            self.codes[digitcode] = digit

    def translateToDigit(self, code):
        return self.codes["".join(sorted(code))]

    def clean(self):
        # some segments are solved, make sure the code is applied to all
        # notposs lists for other values and that they are not present in
        # the poss lists
        solved_letters = [seglist[0] for seglist in self.poss.values() if len(seglist) == 1]

        for seg, letlist in self.poss.items():
            if len(letlist) > 1:
                # check if a solved_letter is present in the list
                for letter in letlist:
                    if letter in solved_letters:
                        self.setSegmentIsNot(seg, letter)
                        self.clean()
                        return


        # we have segments that have letters unique to all segments
        # remove the others from these segments

        # get the 'lonely letters'
        segment_letters = [''.join(seglist) for seglist in self.poss.values()]
        seven_segment_lonely = self.getLonelyLetters(list(''.join(segment_letters)))

        # go through each segment of possible values and remove others if one of the lonely letters is present
        for seg, letlist in self.poss.items():
            # check whether each lonely letter is present
            for lonely_letter in seven_segment_lonely:
                # if a lonely letter is present as well as other letters
                if len(letlist) > 1 and lonely_letter in letlist:
                    # remove the other letters
                    for letter in letlist:
                        if letter is not lonely_letter:
                            self.poss[seg].remove(letter)
                            # start process again because we may have created another lonely letter
                            self.clean()
                            return

    def print(self):
        print("Possible")
        [print(k,l) for k,l in self.poss.items()]
        print("Not possible")
        [print(k,l) for k,l in self.notposs.items()]
        print("Codes ", self.codes)

# end of Ssd class

digcount = {}
number_sum = 0
with open(inputf, 'r') as fh:
    for line in fh:
        #print("\nProcessing ", line)
        line = line.strip()
        bef, aft = line.split(' | ')

        ssd = Ssd(bef)

        # go through each signal (group of segments)
        number = ''
        for digpat in aft.split():

            # Part 1
            # one signal with multiple segments
            segnum = len(digpat)
            if segnum in easy_seg_count:
                if segnum in digcount:
                    digcount[segnum] += 1
                else:
                    digcount[segnum] = 1

            # Part 2
            number += str(ssd.translateToDigit(digpat))
        number_sum += int(number)

print("Part 1")
print("Number of 'easy' digits in input: ", sum(digcount.values()))

print("Part 2")
print("Sum of all decoded numbers: ", number_sum)
