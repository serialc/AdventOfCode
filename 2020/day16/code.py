import re

input_file = 'input_test.txt'
input_file = 'input_test2.txt'
input_file = 'input.txt'

vdict = {}
stage = 0
invalids = []
tvalid = []
mytix = None

with open(input_file, 'r') as fh:
    for line in fh:
        line = line.rstrip()
        if line == "":
            continue

        if line == "your ticket:":
            stage = 1
            continue

        if line == "nearby tickets:":
            stage = 2
            continue

        # build rules in vdict
        if stage == 0:
            label, r1f, r1t, r2f, r2t = re.search("^(.+): (\d+)-(\d+) or (\d+)-(\d+)$", line).groups()
            vdict[label] = [int(r1f), int(r1t), int(r2f), int(r2t)]

        if stage == 1:
            # your ticket, skip for now
            mytix = [int(v) for v in line.split(',')]
            pass

        # check nearby ticket values for validity
        if stage == 2:
            # check each value
            this_ticket_values = []
            for v in line.split(','):
                v = int(v)
                invalid = True
                # look in each vdict
                for lab in vdict:
                    r = vdict[lab]
                    if (v >= r[0] and v <= r[1]) or (v >= r[2] and v <= r[3]):
                        invalid = False
                        break

                if invalid:
                    invalids.append(v)
                    break

            if not invalid:
                # add to list of valid tickets
                tvalid.append([int(v) for v in line.split(',')])


print("Part 1 - The sum of invalid values is ", sum(invalids), "\n\n")

# Part 2
# use mytix, vdict and tvalid to solve

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

labelrow = {}

# for each label
for lab in vdict:
    r = vdict[lab]
    print("Searching for column for label", lab, " rules: ", r)

    # find which column fits in for all tickets
    for coln in range(len(vdict)):
        allfit = True

        # check a column (coln) of values
        vcol = [t[coln] for t in tvalid]
        print("- column ", coln, ' values: ')
        for v in vcol:
            if (v >= r[0] and v <= r[1]) or (v >= r[2] and v <= r[3]):
                print(bcolors.OKBLUE + str(v) + bcolors.ENDC + ' ', end='')
                pass
            else:
                print(bcolors.FAIL + str(v) + bcolors.ENDC + ' ', end='')
                allfit = False

        if allfit:
            if coln in labelrow.values():
                exit("\n\nAlready allocated this column to another label")

            if lab in labelrow:
                labelrow[lab].append(coln)
            else:
                labelrow[lab] = [coln]

        # new line
        print()

print(labelrow)
print([len(labelrow[v]) for v in labelrow])
# So some values fit in multiple columns, need to sudoku this
progsum = sum([len(labelrow[v]) for v in labelrow])
lastsum = 0
constrained_values = []
while progsum != lastsum:
    for label in labelrow:
        if len(labelrow[label]) == 1:
            if labelrow[label][0] not in constrained_values:
                constrained_values.append(labelrow[label][0])
                print("Added", labelrow[label][0], "to CV")
        else:
            for cv in constrained_values:
                if cv in labelrow[label]:
                    labelrow[label].remove(cv)

    print([len(labelrow[v]) for v in labelrow])
    print("Constrained list", constrained_values)
    lastsum = progsum
    progsum = sum([len(labelrow[v]) for v in labelrow])

print(labelrow)

for label in labelrow:
    print(label, labelrow[label])

depproduct = 1
for k in vdict:
    print(k, mytix[labelrow[k][0]])
    if re.match("departure", k):
        depproduct *= mytix[labelrow[k][0]]


print("\nPart 2 - The product of 'departure' starting lines is ", depproduct, "\n\n")
