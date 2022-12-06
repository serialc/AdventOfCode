import numpy as np

with open('input.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:

    winsize = 4 # part 1
    winsize = 14 # part 2
    for line in fh:
        l = line.strip('\n')

        winloc = 0
        while winloc <= len(l) - winsize:
            sopm = l[winloc:winloc+winsize]

            # check for repetition in the start-of-packet marker (sopm)
            dupe = False
            for i in range(len(sopm)-1):
                if sopm[i] in sopm[i+1:len(sopm)]:
                    dupe = True
                    break

            # the sopm has no duplicates, exit loop
            if dupe == False:
                break

            winloc += 1
        

# Part 1
print("#### Part 1 ####")
print("SOPM start: " + str(winloc + winsize))
exit()

################################ PART 2 ######################
print('################################ PART 2 ######################')

with open('input.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:

    for line in fh:
        l = line.strip('\n')

# Part 2
print("#### Part 2 ####")
print("Code: " + '')
