import numpy as np

pdict = {'X': 1, 'Y': 2, 'Z':3}
odict = {'loss':0, 'tie': 3, 'win':6}

score = 0
with open('input.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:
    for line in fh:
        line = line.strip('\n')
        elf, me = line.split(' ')

        # get points for what I play
        score += pdict[me]

        if elf == 'A':
            if me == 'X':
                score += odict['tie']
            if me == 'Y':
                score += odict['win']
            if me == 'Z':
                score += odict['loss']
        if elf == 'B':
            if me == 'X':
                score += odict['loss']
            if me == 'Y':
                score += odict['tie']
            if me == 'Z':
                score += odict['win']
        if elf == 'C':
            if me == 'X':
                score += odict['win']
            if me == 'Y':
                score += odict['loss']
            if me == 'Z':
                score += odict['tie']

# Part 1
print("#### Part 1 ####")
print("Score " + str(score))

################################ PART 2 ######################

edict = {'A': 1, 'B': 2, 'C':3}
score = 0
with open('input.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:
    for line in fh:
        line = line.strip('\n')
        elf, instr = line.split(' ')

        # points for win/tie/loss
        if instr == 'X':
            score += odict['loss']
        elif instr == 'Y':
            score += odict['tie']
        elif instr == 'Z':
            score += odict['win']

        # tie by default
        play = elf
        if elf == 'A':
            if instr == 'X':
                play = 'C'
            if instr == 'Z':
                play = 'B'
        elif elf == 'B':
            if instr == 'X':
                play = 'A'
            if instr == 'Z':
                play = 'C'
        elif elf == 'C':
            if instr == 'X':
                play = 'B'
            if instr == 'Z':
                play = 'A'

        score += edict[play]

# Part 2
print("#### Part 2 ####")
print("Score " + str(score))
