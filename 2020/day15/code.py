import re

input_file = 'input_test.txt'
input_file = 'input.txt'

numage = {}
turn = 1
spoken = None
with open(input_file, 'r') as fh:
    for line in fh:
        line = line.rstrip()

        for num in line.split(','):
            num = int(num)
            numage[num] = [turn]
            spoken = num
            turn += 1
#            print(spoken)

# turn stays what it was
p1 = None
while True:
#    print("Turn ", turn, end='')

    # last number spoken was just said for the first time
    if numage[spoken][0] == (turn - 1):
#        print(" - Last number was new")
        spoken = 0
        numage[spoken].append(turn)
    elif spoken in numage:
#        print(" - Saw number ", spoken, " last spoken ", (turn - 1) - numage[spoken][-2], " turns ago")
        spoken = (turn - 1) - numage[spoken][-2]
        if spoken in numage:
            numage[spoken].append(turn)
        else:
            numage[spoken] = [turn]

#    print(spoken, ',', end='')
    if turn == 2020:
        p1 = spoken
    if turn == 30000000:
        break
    turn += 1

print("Part 1 - Last number spoken is " + str(p1))
print("Part 2 - Last number spoken is " + str(spoken))
