import numpy as np

elf = []
with open('input.txt', 'r') as fh:

    calsum = 0
    for line in fh:
        line = line.strip('\n')

        if line == '':
            elf.append(calsum)
            calsum = 0
        else:
            calsum += int(line)

    # append the last sum
    elf.append(calsum)

# Part 1
npelf = np.array(elf)
elf_max_cal = max(npelf)

print("#### Part 1 ####")
print("Answer is:", elf_max_cal)

# Part 2
npelf.sort()

print("#### Part 2 ####")
print("Answer is:", sum(npelf[-3:]))
