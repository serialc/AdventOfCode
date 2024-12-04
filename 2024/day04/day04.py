import numpy as np
#import re

def matPrint(mat, sep=''):
    nh, nw = mat.shape
    print("Dimension", nh, nw)

    for y in range(nh):
        for x in range(nw):
            print(str(mat[y,x]) + sep, end='')
        print()

input_file = 'input0'
input_file = 'input'

surf = []
with open(input_file, 'r') as fh:
    for l in fh:
        l = l.strip('\n')

        if l == '':
            continue

        surf.append(list(l))

# convert to np
surf = np.array(surf)

# searching for
w = np.array(list('XMAS'))
print("Searching for", w)

# go through whole matrix
# check each configuration
wlen = len(w)
xfound = 0
sh, sw = surf.shape
for y in range(sh):
    for x in range(sh):
        # ease debugging - only process where 'XMAS' could start... at 'X'
        if surf[y,x] != w[0]:
            continue

        # to right
        if x <= (sw - wlen) and np.all(surf[y, x:(x+wlen)] == w):
            xfound += 1
        # to left
        if x >= (wlen - 1) and np.all(surf[y, (x-wlen+1):(x+1)] == w[::-1]):
            xfound += 1
        # down
        if y <= (sh - wlen) and np.all(surf[y:(y+wlen), x] == w):
            xfound += 1
        # up
        if y >= (wlen - 1) and np.all(surf[(y-wlen+1):(y+1), x] == w[::-1]):
            xfound += 1

        # diag - down-right
        if y <= (sh - wlen) and x <= (sw - wlen):
            if np.all(surf[y:(y+wlen), x:(x+wlen)][np.identity(wlen, dtype=bool)] == w):
                xfound += 1

        # diag - down-left
        if y <= (sh - wlen) and x >= (wlen - 1):
            # the identity selection returns values backwards than perhaps expected
            if np.all(surf[y:(y+wlen), (x-wlen+1):(x+1)][np.identity(wlen, dtype=bool)[::-1]] == w):
                xfound += 1

        # diag - up-right
        if y >= (wlen - 1) and x <= (sw - wlen):
            # the identity selection returns values backwards than perhaps expected
            if np.all(surf[(y-wlen+1):(y+1), x:(x+wlen)][np.identity(wlen, dtype=bool)[::-1]] == w[::-1]):
                xfound += 1

        # diag - up-left
        if y >= (wlen -1) and x >= (wlen - 1):
            if np.all(surf[(y-wlen+1):(y+1), (x-wlen+1):(x+1)][np.identity(wlen, dtype=bool)] == w[::-1]):
                xfound += 1

print("#### Part 1 ####")
print("Answer is:", xfound)



#### PART 2 ####
print("============ Part 2 start ================")

# searching for
w = np.array(list('MAS'))
print("Searching for", w)

mascount = np.zeros(surf.shape, dtype=int)

# go through whole matrix
# check each configuration
wlen = len(w)
xfound = 0
sh, sw = surf.shape
for y in range(sh):
    for x in range(sh):
        # ease processing/debugging
        if surf[y,x] != w[0]:
            continue

        # diag - down-right
        if y <= (sh - wlen) and x <= (sw - wlen):
            if np.all(surf[y:(y+wlen), x:(x+wlen)][np.identity(wlen, dtype=bool)] == w):
                mascount[y+1, x+1] += 1
                xfound += 1

        # diag - down-left
        if y <= (sh - wlen) and x >= (wlen - 1):
            # the identity selection returns values backwards than perhaps expected
            if np.all(surf[y:(y+wlen), (x-wlen+1):(x+1)][np.identity(wlen, dtype=bool)[::-1]] == w):
                mascount[y+1, x-1] += 1
                xfound += 1

        # diag - up-right
        if y >= (wlen - 1) and x <= (sw - wlen):
            # the identity selection returns values backwards than perhaps expected
            if np.all(surf[(y-wlen+1):(y+1), x:(x+wlen)][np.identity(wlen, dtype=bool)[::-1]] == w[::-1]):
                mascount[y-1, x+1] += 1
                xfound += 1

        # diag - up-left
        if y >= (wlen -1) and x >= (wlen - 1):
            if np.all(surf[(y-wlen+1):(y+1), (x-wlen+1):(x+1)][np.identity(wlen, dtype=bool)] == w[::-1]):
                mascount[y-1, x-1] += 1
                xfound += 1

matPrint(mascount) 

print("#### Part 2 ####")
print("Answer is:", np.sum(mascount > 1))
