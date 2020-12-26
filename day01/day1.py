import numpy as np

values = []
with open('input.txt', 'r') as fh:
    for line in fh:
       values.append(int(line.strip('\n')))

v = np.array(values)

# Part 1
s = sum(np.meshgrid(v,v))
t = s == 2020
a = np.where(t)[0]

print("#### Part 1 ####")
print("Values are:")
print(v[a])
print("Answer is:")
print(np.prod(v[a]))

# Part 2

s = sum(np.meshgrid(v,v,v))
t = s == 2020
a = np.where(t)[0]

print("#### Part 2 ####")
print("Values are:")
print(v[a][np.array([0,2,4])]) # subsetting
print("Answer is:")
print(np.prod(v[a][np.array([0,2,4])]))
