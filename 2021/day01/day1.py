import numpy as np

values = []
with open('input.txt', 'r') as fh:
    for line in fh:
       values.append(int(line.strip('\n')))


# Part 1
v = np.array(values)
larger_count = sum(np.diff(v) > 0)

print("#### Part 1 ####")
print("Answer is:", larger_count)

# Part 2
nv = []
for i in range(len(values) - 2):
    nv.append(sum(values[i:(i+3)]))

v = np.array(nv)
larger_count = sum(np.diff(v) > 0)

print("#### Part 2 ####")
print("Answer is:", larger_count)
