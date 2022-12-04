import numpy as np

count = 0
with open('input.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:
    for line in fh:
        l = line.strip('\n')
        e1,e2 = l.split(',')
        e1 = e1.split('-')
        e2 = e2.split('-')

        # create a list of the numbers for each elf
        e1 = [x for x in range(int(e1[0]), int(e1[1])+1)]
        e2 = [x for x in range(int(e2[0]), int(e2[1])+1)]

        # look if any of elf2's tasks are not in elf1's task list
        xcont = True
        for x in e1:
            if x not in e2:
                xcont = False
                break

        # as above, but opposite
        ycont = True
        for y in e2:
            if y not in e1:
                ycont = False
                break

        # check if either is overlaped
        if xcont or ycont:
            print("Complete overlap at: " + l)
            count += 1

# Part 1
print("#### Part 1 ####")
print("Score " + str(count))

################################ PART 2 ######################
print('################################ PART 2 ######################')

count = 0
with open('input.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:
    for line in fh:
        l = line.strip('\n')
        e1,e2 = l.split(',')
        e1 = e1.split('-')
        e2 = e2.split('-')
        print(l)

        e1 = [x for x in range(int(e1[0]), int(e1[1])+1)]
        e2 = [x for x in range(int(e2[0]), int(e2[1])+1)]

        # just count if there is any overlap
        for x in e1:
            if x in e2:
                count += 1
                print(l)
                break

# Part 2
print("#### Part 2 ####")
print("Score " + str(count))
