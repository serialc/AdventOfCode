import numpy as np

def printV(m):
    if m.ndim == 1:
        # vector
        for b in m:
            if b == 1:
                print('#', end='')
            else:
                print('.', end='')
        print()
    else:
        # matrix
        for r in range(m.shape[0]):
            for c in range(m.shape[1]):
                if m[r,c] == 1:
                    print('.', end='')
                else:
                    print('#', end='')
            print()


#with open('input.txt', 'r') as fh:
with open('test_input.txt', 'r') as fh:

    x = 1
    c = 0
    cs = 0

    vals = []

    for line in fh:

        l = line.strip('\n')
        print('line', l, 'state x=', x, 'c=', c)

        icc = 1
        if l != 'noop':
            icc = 2

        while icc > 0:
            v = np.zeros(40, dtype=int)
            v[x-1:x+2] = 1
            printV(v)
            printV(np.array(vals))

            if v[c%40] == 0:
                vals.append(1)
            else:
                vals.append(0)

            c += 1
            icc -= 1
            if (c-20)%40 == 0:
                print('round', c*x, c, x)
                cs += c*x


        # it's an add instruction, 2 cycles finished, add to it
        if l != 'noop':
            x += int(l.split(' ')[1])


# Part 1
print("#### Part 1 ####")
print("Part 1 answer: " + str(cs))

################################ PART 2 ######################
print('################################ PART 2 ######################')

# Part 2
print("#### Part 2 ####")
m = np.array(vals, dtype=int).reshape(6,40)
printV(m)
print("Part 2 answer: " + str(cs))

