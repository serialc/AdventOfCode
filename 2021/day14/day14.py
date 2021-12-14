import numpy as np
import time
#from PIL import Image

inputf = 'test_input'
inputf = 'input'

rules = dict()
templ = []

### Read input data
with open(inputf, 'r') as fh:
    for line in fh:
        line = line.strip()

        if line == "":
            continue

        if line[0] == "#":
            continue

        if len(templ) == 0:
            templ = list(line)
            continue

        r, ins = line.split(" -> ")
        rules[r] = ins

def getResult(steps, templ, rules):

    for s in range(steps):
        ntempl = []
        for i in range(len(templ) - 1):
            pair = "".join(templ[i:(i+2)])

            ntempl.append(templ[i])
            if pair in rules:
                ntempl.append(rules[pair])

        # need to add the last element
        ntempl.append(templ[-1])
        templ = ntempl.copy()

    el, freq = np.unique(np.array(templ), return_counts=True)
    fmax = np.max(freq)
    fmin = np.min(freq)
    return fmax - fmin

### Part 1
print("###### Part 1")
start = time.time()
print("Result", getResult(10, templ.copy(), rules))
end = time.time()
print("Processing time", end - start)

### Part 2
print("\n###### Part 2")
# Can't use the same ineffecient algorithm as before
# let's try building the tree from the leaves (rules) to the trunk (template)
# rather than the other way around

start = time.time()

# helper function to merge values from two dictionary 
def mergeDict(a, b, remove):
    for ak,av in a.items():
        if ak in b:
            b[ak] += av
        else:
            b[ak] = av
    b[remove] -= 1
    return b

# create the leaves
code_depth_freq_dict = {}
for ab, ins in rules.items():
    nab = ab[0] + ins + ab[1]
    tdict = dict()
    el, freq = np.unique(np.array(list(nab)), return_counts=True)
    for i in range(len(el)):
        tdict[el[i]] = freq[i]
    code_depth_freq_dict[ab] = tdict

#[print(k,v) for k,v in code_depth_freq_dict.items()]

# iterate up, from the leaves back to the trunk of letter pairs
for d in range(1,40):
    #print("Depth", d)
    ncdf = {}
    for ab, fab in code_depth_freq_dict.items():
        for bc, fbc in code_depth_freq_dict.items():
            # where the b matches in ab and bc
            # and ac is a rule that creates abc
            ac = ab[0] + bc[1]
            if ab[1] == bc[0] and ac in rules and rules[ac] == ab[1]:
                #print("Join", ab, bc, "as", ab[0] + bc[-1], "with distributions of")
                #print(fab, fbc, "summed to", mergeDict(fab.copy(), fbc.copy(), ab[1]))
                ncdf[ac] = mergeDict(fab.copy(), fbc.copy(), ab[1])
    code_depth_freq_dict = ncdf.copy()

# now go through top level code pairs and build up frequencies
freq_sum = {}
# get max and min from our value frequency table
for i in range(len(templ) - 1):
    pair = "".join(templ[i:(i+2)])
    freq_sum = mergeDict(freq_sum.copy(), code_depth_freq_dict[pair].copy(), pair[1])
# handle last letter
freq_sum[pair[1]] += 1

freq = list(freq_sum.values())
fmax = max(freq)
fmin = min(freq)
print("Part2 answer", fmax - fmin)
end = time.time()
print("Processing time", end - start)
