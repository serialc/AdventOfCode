import numpy as np

input_file = 'test_input'
input_file = 'input'

# load data
td = np.loadtxt(input_file, dtype='str')

#### Part 1

# reshape to matrix
nd = []
for word in td:
    nd.append([int(char) for char in word])
m = np.array(nd)

gamma = ''
epsi = ''
for i in range(m.shape[1]):
    gamma += str(int(np.mean(m[:,i]) + 0.5))

def invertBinary(bstr):
    bstr = str(bstr)
    return ''.join(['1' if b == '0' else '0' for b in bstr])

epsi = invertBinary(gamma)

dgamma = int(gamma,2)
depsi  = int(epsi,2)

print("Part 1 answer is: " + str(dgamma * depsi))

#### Part 2
print("======== Part 2 ===========")

def getBitMode(mat, common_or_not, bitofinterest):
    val = int(np.mean(mat[:,bitofinterest]) + 0.5)
    if val == 0.5:
        val = str(val)
    else:
        str(int(val))
    if common_or_not == 'common':
        return val
    else:
        return invertBinary(val)

def process(matofi, com_uncom, pref):

    boi = 0
    # keep popping the less common
    while np.shape(matofi)[0] > 1:
        # get the most common first bit
        commonbit = getBitMode(matofi, com_uncom, boi)

        if commonbit == '0.5':
            commonbit = pref

        # keep only the rows that start with commonbit
        matofi = matofi[matofi[:,boi] == int(commonbit)]

        boi += 1
    return matofi

oxmat = process(np.copy(m), 'common', 1)
o2mat = process(np.copy(m), 'uncommon', 0)

dox = int(''.join([str(x) for x in oxmat[0]]),2)
do2 = int(''.join([str(x) for x in o2mat[0]]),2)

print("Part 2 answer is: ", dox, do2, dox*do2)
