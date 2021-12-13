import numpy as np
from PIL import Image

inputf = 'test_input'
inputf = 'input'

dots  = []
instr = []
mode  = 1
### Read input data
with open(inputf, 'r') as fh:
    for line in fh:
        line = line.strip()
        if line == "":
            mode = 2
            continue
        if mode == 1:
            dots.append(line.split(','))
        if mode == 2:
            axis, linenum = line.split(' ')[2].split('=')
            instr.append([axis, int(linenum)])

dots = np.array(dots, dtype=int)
w,h = np.max(dots, axis=0) + 1

imap = np.zeros((h,w), dtype=int)

for i in range(dots.shape[0]):
    x,y = dots[i,:]
    imap[y,x] = 1

# start folding
def fold(m, ax, i):
    #print(m.shape, ax, i)
    if ax == 'y':
        # there is one 'bad' fold that isn't in the middle!
        if i != int(m.shape[0]/2):
            fold_size = m.shape[0] - i
            unused = h - 2*fold_size + 1
            foldedpart = np.logical_or(m[unused:i, :], np.flip(m[i+1:, :],0))
            folded = np.concatenate((m[:unused, :], foldedpart*1), axis=0)
        else:
            folded = np.logical_or(m[:i, :], np.flip(m[i+1:, :],0))
    if ax == 'x':
        folded = np.logical_or(m[:, :i], np.flip(m[:, i+1:],1))
    folded = folded*1

    return folded

### Part 1
print("\n###### Part 1")

fmap = imap.copy()
for axis, linenum in instr:
    fmap = fold(fmap, axis, linenum)
    print(np.sum(fmap))
    break

### Part 2
print("\n###### Part 2")
fmap = imap.copy()
for axis, linenum in instr:
    fmap = fold(fmap, axis, linenum)

for y in range(fmap.shape[0]):
    for x in range(fmap.shape[1]):
        if fmap[y,x] == 0:
            print('.', end='')
        else:
            print('#', end='')
    print('')
#print(fmap)
