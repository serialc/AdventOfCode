import re
import numpy as np
import math

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

input_file = 'input_test'
#input_file = 'input_test2'
input_file = 'input'

# player one/two decks
pod = []
ptd = []
with open(input_file, 'r') as fh:
    row = 0
    mode = 1
    for line in fh:
        line = line.rstrip()

        if line == "":
            mode = 2

        rem = re.match("(\d+)", line)
        if rem:
            if mode == 1:
                pod.append(int(rem.groups()[0]))
            if mode == 2:
                ptd.append(int(rem.groups()[0]))


# saves player deck configurations
# to prevent endless recursion
ppod = {}
pptd = {}

def rround(rpod, rptd, gnum):
    ''' Returns the modified decks '''

    # check we've never played this configuration before
    poh = "-".join([str(n) for n in rpod])
    pth = "-".join([str(n) for n in rptd])

    if gnum in ppod and gnum in pptd and poh in ppod[gnum] and pth in pptd[gnum]:
        print("Recursion exit, have already seen these hands in this (sub)game")
        return "P1WIN"

    # save both player decks to past played sets
    if gnum in ppod and gnum in pptd:
        ppod[gnum].append(poh)
        pptd[gnum].append(pth)
    else:
        ppod[gnum] = [poh]
        pptd[gnum] = [pth]

    poc = rpod.pop(0)
    ptc = rptd.pop(0)
    print("Player 1 plays:",poc)
    print("Player 2 plays:",ptc)

    # determine if we go to a new subgame
    if len(rpod) >= poc and len(rptd) >= ptc:
        print("Playing into sub-game to determine the winner...")
        if rgame(rpod[:poc], rptd[:ptc]) == 1:
            rpod.append(poc)
            rpod.append(ptc)
        else:
            rptd.append(ptc)
            rptd.append(poc)
        print("...anyway, back to game",gnum,"\n")
    else:
        if poc > ptc:
            rpod.append(poc)
            rpod.append(ptc)
        if poc < ptc:
            rptd.append(ptc)
            rptd.append(poc)

    return [rpod,rptd]

gnumdisp = 1
def rgame(rpod, rptd):
    ''' Returns the integer of the winning player '''
    global gnumdisp
    gnum = gnumdisp
    gnumdisp += 1

    gameround = 1
    print("\n=== Game", gnum,"===\n")
    while len(rpod) > 0 and len(rptd) > 0:
        print("-- Round", gameround," (Game", str(gnum) + ") --")
        print("Player 1's deck:", rpod)
        print("Player 2's deck:", rptd)

        rres = rround(rpod, rptd, gnum)
        if rres == "P1WIN":
            break
        else:
            rpod, rptd = rres

        gameround += 1

    if rres == "P1WIN" or len(rpod) > len(rptd):
        print("The winner of game", gnum, "is player 1!\n")
        return 1
    else:
        print("The winner of game", gnum, "is player 2!\n")
        return 2

rgame(pod, ptd)

if len(pod) > len(ptd):
    windeck = pod
else:
    windeck = ptd

winscore = 0
for i in range(len(windeck)):
    winscore += windeck[i] * (len(windeck) - i)

print("== Post-game results ==")
print("Player 1's deck:", pod)
print("Player 2's deck:", ptd)
print("Part 2 - Winning score is", winscore)
