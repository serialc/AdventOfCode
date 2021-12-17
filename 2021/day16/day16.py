import numpy as np
#import time
#from PIL import Image
import sys

#print("Recursion limit", sys.getrecursionlimit())

inputf = 'test_input'
inputf = 'test_input2'
inputf = 'test_input3'
inputf = 'test_input4'
inputf = 'input'

def hex2bin(hexval, bits):
    return bin(int(hexval, 16))[2:].zfill(bits)

def bin2int(binval):
    return int(binval, 2)

def getNumber(bline, pi):
    readp = True
    lit = ""
    while readp:
        if bline[pi] == '0':
            readp = False

        lit += bline[pi+1:pi+5]
        pi += 5
    # bump up until we reach the end of the 4-bit group
    #while pi%4 != 0:
    #    pi += 1
    return bin2int(lit), pi

### Read input data
with open(inputf, 'r', encoding='utf-8-sig') as fh:
    for line in fh:
        hexline = line.strip()

#hexline = 'C200B40A82'
#hexline = '04005AC33890'
#hexline = '880086C3E88112'
#hexline = 'CE00C43D881120'
#hexline = 'D8005AC2A8F0'
#hexline = 'F600BC2D8F'
#hexline = '9C005AC2F8F0'
#hexline = '9C0141080250320F1802104A08'

bline = ''
for hexchar in list(hexline):
    bline += hex2bin(hexchar,4)

version_sum = 0
def processPacket(bline, sp_specified=False, sp_contained=0):
    global version_sum
    values = []

    bli = 0
    sp_count = 0
    while bli < len(bline):
        print("\nProcess", bline[bli:])
        version = bin2int(bline[bli:bli+3])
        version_sum += version
        bli += 3
        pid = bin2int(bline[bli:bli+3])
        bli += 3

        print("Version", version)
        print("PID", pid)

        if pid == 4:
            # literal/number packet
            num, bli = getNumber(bline, bli)
            values.append(num)
            print("Added number", num, "to values", values)
        else:
            # operator packet (contains one or more packets)
            print("Operator packet")

            # get the length type ID
            ltid = bline[bli]
            print("Length type ID", ltid)
            bli += 1
            plen = 0

            # length type ID
            if ltid == '0':
                print("15 bits")
                splen = bin2int(bline[bli:bli+15])
                bli += 15
                print("Sub Packet(s) length", splen)
                ret_values = processPacket(bline[bli:bli+splen])
                values.append(ret_values)
                bli += splen
            if ltid == '1':
                print("11 bits")
                spnum = bin2int(bline[bli:bli+11])
                bli += 11
                print("Number of sub Packets", spnum)

                # process subpacket of unknown length
                # returns the end of the bline that is not yet processed
                ret_values, bline = processPacket(bline[bli:], True, spnum)
                values.append(ret_values)
                # need to reset bli to 0
                bli = 0

            # process the number available given the operator
            print("Perform operation", pid, "on values", values,"in version",version)
            if pid == 0:
                # sum
                this_sum = 0
                for spv in values.pop():
                    this_sum += spv
                values.append(this_sum)

            if pid == 1:
                # product
                this_prod = 1
                for spv in values.pop():
                    this_prod *= spv
                values.append(this_prod)

            if pid == 2:
                # min
                this_min = 9999999
                for spv in values.pop():
                    if spv < this_min:
                        this_min = spv

                values.append(this_min)
            if pid == 3:
                # max
                this_max = -9999999
                for spv in values.pop():
                    if spv > this_max:
                        this_max = spv
                values.append(this_max)

            if pid == 5:
                # first is greater than second => 1 else 0
                first, second = values.pop()
                if first > second:
                    values.append(1)
                else:
                    values.append(0)

            if pid == 6:
                # first is less than second => 1 else 0
                first, second = values.pop()
                if first < second:
                    values.append(1)
                else:
                    values.append(0)

            if pid == 7:
                # equal => 1 else 0
                first, second = values.pop()
                if first == second:
                    values.append(1)
                else:
                    values.append(0)

        # count, necessary if parent packet is of length type ID of 1
        sp_count += 1
        if sp_specified and sp_count == sp_contained:
            # return rest of binary string
            print("Process version",version,"returning value", values)
            return values, bline[bli:]

        # end if only '0' remain
        if '1' not in list(bline[bli:]):
            print("Process version",version,"returning value", values)
            return values

result = processPacket(bline)

# first 3 bits - version
# next 3 bits - type ID
# ID=4, value

### Part 1
print("=========== PART 1 ===============")
print("Part 1 answer", version_sum)

### Part 2
print("=========== PART 2 ===============")
print("Part 2 answer", result)
