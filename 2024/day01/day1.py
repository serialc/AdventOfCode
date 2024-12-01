input_file = 'input0'
input_file = 'input'

l1 = []
l2 = []

with open(input_file, 'r') as fh:
    for l in fh:
        l = l.strip('\n')

        if l == '':
            continue

        p = l.split('   ');
        l1.append(int(p[0]))
        l2.append(int(p[1]))

l1.sort()
l2.sort()

ldiffsum = 0
for i in range(len(l1)):
    ldiffsum += abs(l1[i] - l2[i])

print("#### Part 1 ####")
print("Answer is:", str(ldiffsum))

#### PART 2 ####
print("============ Part 2 start ================")

# build a frequency dictionary
l2freq = dict()
for v in l2:
    if v in l2freq:
        l2freq[v] += 1
    else:
        l2freq[v] = 1

p2sum = 0
for v in l1:
    if v in l2freq:
        p2sum += v * l2freq[v]

print("#### Part 2 ####")
print("Answer is:", str(p2sum))
