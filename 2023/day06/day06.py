#from math import prod
import numpy as np
import re

input_file = 'input0'
input_file = 'input'

with open(input_file, 'r') as fh:
    lines = []
    for l in fh:
        l = l.strip('\n')
        lines.append(list(map(int, l.split()[1:])))

# reshape
races = [[lines[0][x],lines[1][x]] for x in range(len(lines[0]))]

racewins = []
raceprod = 1
for t,dr in races:
    print(t,dr)

    wins = 0
    for s in range(t+1):
       rt = t - s
       d = s * rt
       if d > dr:
           wins += 1

    racewins.append(wins)
    raceprod *= wins

print(racewins)

print("#### Part 1 ####")
print("Answer is:", raceprod)

#### PART 2 ####
print("============ Part 2 start ================")

with open(input_file, 'r') as fh:
    lines = []
    for l in fh:
        l = l.strip('\n')
        lines.append(''.join(l.split()[1:]))


t = int(lines[0])
dr = int(lines[1])

wins = 0
for s in range(t+1):
   rt = t - s
   d = s * rt
   if d > dr:
       wins += 1

print("#### Part 2 ####")
print("Answer is:", wins)
