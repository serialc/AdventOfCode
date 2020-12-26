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


def pround():
    poc = pod.pop(0)
    ptc = ptd.pop(0)

    if poc > ptc:
        pod.append(poc)
        pod.append(ptc)
    if poc < ptc:
        ptd.append(ptc)
        ptd.append(poc)

while len(pod) > 0 and len(ptd) > 0:
    pround()
    print("Player1:", pod)
    print("Player2:", ptd)


if len(pod) > len(ptd):
    windeck = pod
else:
    windeck = ptd

winscore = 0
for i in range(len(windeck)):
    winscore += windeck[i] * (len(windeck) - i)

print("Part 1 - Winning score is", winscore)
