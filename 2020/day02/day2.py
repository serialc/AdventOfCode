import re

valid = 0
valid2 = 0
with open('input.txt', 'r') as fh:
    for line in fh:
        # clean and split
        crit, pw = line.strip('\n').split(': ')

        # further splitting into range and char
        critmin, critmax, critchar = re.split('-| ', crit)
        critmin = int(critmin)
        critmax = int(critmax)

        # PART 1
        count = 0
        for char in pw:
            if char == critchar:
                count += 1

        if count >= critmin and count <= critmax:
            valid += 1

        # PART 2
        if (pw[critmin-1] == critchar and pw[critmax-1] != critchar) or \
                (pw[critmin-1] != critchar and pw[critmax-1] == critchar):
            valid2 += 1


# how many passwords are valid?
print("Found " + str(valid) + " valid PART 1 passwords.")
print("Found " + str(valid2) + " valid PART 2 passwords.")
