
true_valid = 0
valid = 0

parts =     ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
req_parts = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

passports = []
passport = dict()

def check_valid(passport):
    global parts, valid, true_valid

    if len(parts) == len(passport):
        true_valid += 1
        valid += 1

    if 'cid' not in passport and len(passport) == (len(parts) - 1):
        valid += 1

with open('input.txt', 'r') as fh:
    for line in fh:
        line = line.rstrip()
        #print(line)

        # Finished a passport
        if line == '':
            check_valid(passport)

            passports.append(passport)
            passport = dict()
            continue

        # add data to passport dict
        for part in line.split(' '):
            code,val = part.split(':')
            passport[code] = val

# catch the last passport
check_valid(passport)
passports.append(passport)

# display results
print("Found " + str(len(passports)) + " passports.")
print("Dubiously 'valid': " + str(valid))
print("True valid: " + str(true_valid))

# PART 2
import re
vpp = []

print("\n\nPart 2")

p2_valid = 0
maxbyr = 0
minbyr = 99999999999

for passport in passports:
    # it must have at least the seven fields
    if (len(passport) < len(parts) and 'cid' in passport) or \
            ('cid' not in passport and len(passport) < (len(parts) - 1)):
        print("Missing fields - length: " + str(len(passport)) + ". " +\
            "Has cid: " + str('cid' in passport))
        continue

    # birth year
    byr = int(passport['byr'])
    if byr < 1920 or byr > 2002:
        print("Birth Year not valid: " + str(byr))
        continue
    else:
        if byr < minbyr:
            minbyr = byr
        if byr > maxbyr:
            maxbyr = byr

    # issue year
    iyr = int(passport['iyr'])
    if iyr < 2010 or iyr > 2020:
        print("Issue Year not valid: " + str(iyr))
        continue

    # expiration year
    eyr = int(passport['eyr'])
    if eyr < 2020 or eyr > 2030:
        print("Expiration Year not valid: " + str(eyr))
        continue

    # height
    height = passport['hgt']
    hgt = re.search('(\d+)(cm|in)$', height)

    # must match to be valid
    if hgt:
        val = int(hgt.groups()[0])
        if hgt.groups()[1] == 'cm' and \
                (val < 150 or val > 193):
            print("CM - wrong height: " + height)
            continue
        if hgt.groups()[1] == 'in' and \
                (val < 59 or val > 76):
            print("IN - wrong height: " + height)
            continue
    else:
        print("Badly formatted height: " + height)
        continue

    # hair colour
    if not re.match("\#[a-f0-9]{6}$", passport['hcl']):
        print("Hair colour not valid: " + passport['hcl'])
        continue

    # eye colour
    if passport['ecl'] not in ['amb','blu','brn','gry','grn','hzl','oth']:
        print("Eye colour not valid: " + passport['ecl'])
        continue

    # passport number
    if not re.match("\d{9}$", passport['pid']):
        print("PID not valid: " + passport['pid'])
        continue

    # passed all tests
    p2_valid += 1
    #print(passport)
    vpp.append(passport)

print("\n\nValid passports: " + str(p2_valid))
print("Max byr: " + str(maxbyr))
print("Min byr: " + str(minbyr))

exit()
for passport in vpp:
    for part in req_parts:
        print(passport[part] + "\t", end="")
    print("")

