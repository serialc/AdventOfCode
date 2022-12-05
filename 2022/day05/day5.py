import numpy as np

with open('input.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:

    mode = 'stacks'
    s = {}

    for line in fh:
        l = line.strip('\n')

        if l == "":
            mode = "instructions"
            continue

        if mode == "instructions":
            ins = l.split(' ')
            rep = int(ins[1])
            fstck = int(ins[3])
            dstck = int(ins[5])

            # move from one stack to another
            for t in range(rep):
                s[dstck].append(s[fstck].pop())

        pos = 1
        stack = 1

        if mode == "stacks":
            while pos < len(l):
                if l[pos] == " ":
                    pass
                elif not l[pos].isalpha():
                    # we are at the bottom of the stacks/numbers
                    break
                else:
                    # create list/stack (in dict) if doesn't yet exist
                    if stack not in s:
                        s[stack] = []

                    s[stack].insert(0, l[pos])

                stack += 1
                pos += 4

# get the code by popping in order
code = ''
for i in range(1, len(s) + 1):
    code += s[i].pop()

# Part 1
print("#### Part 1 ####")
print("Code: " + code)

################################ PART 2 ######################
print('################################ PART 2 ######################')

with open('input.txt', 'r') as fh:
#with open('test_input.txt', 'r') as fh:
    mode = 'stacks'
    s = {}

    for line in fh:
        l = line.strip('\n')

        if l == "":
            mode = "instructions"
            continue

        if mode == "instructions":
            ins = l.split(' ')
            rep = int(ins[1])
            fstck = int(ins[3])
            dstck = int(ins[5])

            print("Move " + str(rep) + " from " + str(fstck) + " to " + str(dstck))

            # move from one stack to another
            hold = []
            # move into hold in reversed order
            for t in range(rep):
                hold.append(s[fstck].pop())

            # move hold contents back in, in correct order
            while len(hold) > 0:
                s[dstck].append(hold.pop())

        pos = 1
        stack = 1

        if mode == "stacks":
            while pos < len(l):
                if l[pos] == " ":
                    pass
                elif not l[pos].isalpha():
                    # we are at the bottom of the stacks/numbers
                    break
                else:
                    # create list/stack (in dict) if doesn't yet exist
                    if stack not in s:
                        s[stack] = []

                    s[stack].insert(0, l[pos])

                stack += 1
                pos += 4

# get the code by popping in order
code = ''
for i in range(1, len(s) + 1):
    code += s[i].pop()

# Part 2
print("#### Part 2 ####")
print("Code: " + code)
