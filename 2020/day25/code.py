#import re
#import numpy as np
#import math
#import time
#from PIL import Image

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

buildlim = 50000000
subjectnum = 7

cpk = None
dpk = None
with open(input_file, 'r') as fh:
    for line in fh:
        line = line.rstrip()

        if cpk is None:
            cpk = int(line)
            continue
        if dpk is None:
            dpk = int(line)
            continue

print("Card public key", cpk)
print("Door public key", dpk)
        
cryptoarray = [None]*(buildlim+1)
lastcrypt = 1
for i in range(1, buildlim):
    lastcrypt = (lastcrypt * subjectnum) % 20201227
    cryptoarray[i] = lastcrypt

def transform(sn, ls):
    val = 1
    for i in range(ls):
        val = (val * sn) % 20201227
    return val

cpkls = cryptoarray.index(cpk)
dpkls = cryptoarray.index(dpk)

print("Loop size for public key " + str(cpk) + " is:" + str(cpkls))
print("Loop size for public key " + str(dpk) + " is:" + str(dpkls))

print("Encrypted key is:" + str(transform(dpk, cpkls)) )
