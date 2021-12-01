import re
import numpy as np

input_file = 'input_test.txt'
input_file = 'input_test2.txt'
input_file = 'input_test3.txt'
input_file = 'input.txt'

# create list of possible strings
rdict = {}
msglist = []
msgmode = False
with open(input_file, 'r') as fh:
    ypos = None
    for line in fh:
        line = line.rstrip()

        if line == "":
            msgmode = True
            continue

        # part 2 replace rules
        if line == "11: 42 31":
            line = "11: 42 31 | 42 11 31"
        if line == "8: 42":
            line = "8: 42 | 42 8"

        if msgmode:
            msglist.append(line)
            continue

        charm = re.match('(\d+)\: "(\w+)"$', line)
        if charm:
            rdict[int(charm.groups()[0])] = ['c', charm.groups()[1]]
            continue

        recp = line.split(": ")
        rdict[int(recp[0])] = ['r', recp[1].split(" | ")]

#print("Rule dictionnary:",rdict, "\n")
#print("Message list:", msglist, "\n\n")
print("Message list has length:", len(msglist))

def bcode(rule, lvl):

    lvlpad = " "*lvl
#   print(lvlpad + "rule", rule)

    if rule == 8:
        return ['8']
    if rule == 11:
        return ['11']

    instr = rdict[rule]
    # character
    if instr[0] == 'c':
#        print(lvlpad + ' <- ', instr[1])
        return [instr[1]]

    # rule(s)
    if instr[0] == 'r':

        # list of 'OR' lists
        codelist = []
        for rset in instr[1]:

            code = []
            # one set of sequential codes
            for r in rset.split(' '):

                # can return a character or list of characters
                recvd = bcode(int(r), lvl + 1)

                # need to join to existing list
                if len(code) == 0:
                    code = recvd[:]
                    continue
                if len(recvd) == 1 and len(code) == 1:
                    code = [code[0] + recvd[0]]
                    continue
                ncode = []
#                print(lvlpad + "With:", code, recvd)
                for c in code:
                    for rcode in recvd:
                        ncode.append(c + rcode)
#                print(lvlpad + "Combined codes to:", ncode)
                code = ncode[:]

#            print(lvlpad + "R,I,CL,C", rule, instr, codelist, code)
            codelist += code
#        print(lvlpad + ' <- ', codelist)
        return codelist

# generate list of valid codes
#vcodes = bcode(0,0)
c42 = bcode(42,0)
c31 = bcode(31,0)

# solve for 0: 8 11
# given:
# 8: 42 | 42 8
# 11: 42 31 | 42 11 31
# so must be a sequence of c42, followed by a sequence of c31

#print("Valid 31 codes:",c31)
#print("Valid 42 codes:",c42)

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

# check messages and count number of valid ones
vcount = 0
chunksize = len(c31[0])

for msgn in range(len(msglist)):
    msg = msglist[msgn]
#    print("Checking message '" + msg + "', length =", len(msg))

    if len(msg)%chunksize != 0:
        print("Skipping message '" + msg + "' as it is the wrong length.")
        continue

    stg = 0
    c1 = 0
    c2 = 0

    validmsg = True

    # all chunks are chunksize long
    while len(msg) > 0:
        chunk = msg[0:chunksize]
        msg = msg[chunksize:]
#        print("\nchunk:",chunk,"msg:",msg,"stage:",stg)
        if stg == 0:
#            print("chunk", stg, chunk)
            if chunk in c42:
                c1 += 1
                print(bcolors.OKBLUE + chunk + bcolors.ENDC + ' ', end='')
                continue
            if c1 == 0:
                validmsg = False
                print(bcolors.FAIL + chunk + bcolors.ENDC + ' ', end='')
                print(bcolors.FAIL + msg + bcolors.ENDC + ' ', end='')
                break
            stg = 1

        if stg == 1:
#            print("chunk", stg, chunk)
            if chunk in c31:
                c2 += 1
                print(bcolors.OKGREEN + chunk + bcolors.ENDC + ' ', end='')
                continue
            else:
                # there may be more stuff at the end, other metrics don't check this
                validmsg = False
                print(bcolors.FAIL + chunk + bcolors.ENDC + ' ', end='')
                print(bcolors.FAIL + msg + bcolors.ENDC + ' ', end='')
                break
    
    if validmsg and len(msg) == 0 and c1 >= 1 and c2 >= 1:
        if c1 > c2:
            print(bcolors.BOLD + " Valid!" + bcolors.ENDC, c1, c2, len(msglist[msgn]))
            vcount += 1
        else:
            print( bcolors.FAIL + " Unbalanced invalidation!" + bcolors.ENDC, c1, c2)
    else:
        print( bcolors.FAIL + " Invalid!" + bcolors.ENDC, c1, c2)

print("\n\nPart 2 results of valid codes are:", vcount)
