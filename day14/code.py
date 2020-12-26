import re

input_file = 'input_test.txt'
input_file = 'input_test2.txt'
input_file = 'input.txt'

def maskit(val, m):
    bval = str(bin(val)[2:])
    # make it same length as mask
    bval = '0'*(len(m) - len(bval)) + bval

    for b in range(len(m)-1,-1,-1):
        if m[b] == 'X':
            continue
        if m[b] == '1':
            bval = bval[:b] + '1' + bval[(b+1):]
        if m[b] == '0':
            bval = bval[:b] + '0' + bval[(b+1):]

    return bval


memory = {}
mask = ''
with open(input_file, 'r') as fh:
    for line in fh:
        line = line.rstrip()

        if line[:4] == 'mask':

            mask = line[7:]
            continue

        mem, val = re.search('mem\[(\d+)\] = (\d+)', line).groups()

        memory[mem] = maskit(int(val), mask)

memsum = 0
for addr in memory:
    memsum += int(memory[addr],2)

print("Part 1 - Sum of memory is " + str(memsum) + "\n\n")


print("Part 2 start")

def maskit2(val, m):
    bval = str(bin(val)[2:])
    # make it same length as mask
    bval = '0'*(len(m) - len(bval)) + bval

    for b in range(len(m)-1,-1,-1):
        if m[b] == 'X':
            bval = bval[:b] + 'X' + bval[(b+1):]
        if m[b] == '1':
            bval = bval[:b] + '1' + bval[(b+1):]
        if m[b] == '0':
            continue

    return bval

# reset memory
memory = {}
mask = ''
with open(input_file, 'r') as fh:
    for line in fh:
        line = line.rstrip()

        if line[:4] == 'mask':
            mask = line[7:]
            continue

        mem, val = re.search('mem\[(\d+)\] = (\d+)', line).groups()

        # get the address with 'X' as floating bits
        floatbits = maskit2(int(mem), mask)

        # how many floating bits
        fbitsn = floatbits.count('X')

        # build all the variations of addresses
        for i in range(pow(2, fbitsn)):

            # for this iteration get the 0/1 combination
            fval = bin(i)[2:]
            # front pad so it's the correct/consistent length
            fval = '0'*(fbitsn - len(fval)) + fval
            # turn to list so we can pop(0) from front of list
            fval = [char for char in fval]

            # fill this
            fbaddr = ''
            for b in floatbits:
                if b == 'X':
                    fbaddr += fval.pop(0)
                else:
                    fbaddr += b

            #print(fbaddr, ' ', len(fbaddr))
            memory[fbaddr] = int(val)

sumval = 0
print("memory size=", len(memory))
for addr in memory:
    sumval += memory[addr]
print("Part 2 - Values in memory sum is " + str(sumval))
