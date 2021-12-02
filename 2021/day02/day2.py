import numpy as np


values = []
with open('input.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:
    for line in fh:
        lv = line.strip('\n')
        cmd, mag = lv.split(' ')
        mag = int(mag)
        values.append([cmd, mag])

# Part 1
print("#### Part 1 ####")

pos = 0
depth = 0
for cmd, mag in values:
    if cmd == "forward":
        pos += mag
    elif cmd == "down":
        depth += mag
    elif cmd == "up":
        depth -= mag
        if depth < 0:
            depth = 0

print('pos =',pos, 'depth =',depth)
print("Answer is:", pos*depth)

# Part 2
print("#### Part 2 ####")

aim = 0
pos = 0
depth = 0
for cmd, mag in values:
    if cmd == "forward":
        pos += mag
        depth += aim * mag
    elif cmd == "down":
        aim += mag
    elif cmd == "up":
        aim -= mag
        if depth < 0:
            depth = 0


print("Answer is:", pos*depth)
