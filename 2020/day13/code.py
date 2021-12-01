# day 11
import math

input_file = 'input_test.txt'
input_file = 'input_test2.txt'
input_file = 'input.txt'

ts = None
buses = []
busdict = {}

with open(input_file, 'r') as fh:
    for line in fh:
        line = line.rstrip()

        if ts is None:
            ts = int(line)
            continue

        buses = line.split(',')

print("Time is " + str(ts))
print("Buses", buses)

for bus in buses:
    if bus == 'x':
        continue

    busnum = int(bus)
    busdict[busnum] = busnum - ts%busnum

nextbus = None
for busnum in busdict:
    print("Bus " + str(busnum) + " departs in " + str(busdict[busnum]) + " minutes.")
    if nextbus == None or busdict[busnum] < busdict[nextbus]:
        nextbus = busnum

print("Part 1 - Bus " + str(nextbus) + " departs in " + str(busdict[nextbus]) + " minutes. Code is: " + str(nextbus * busdict[nextbus]) + "\n\n")



# Part 2
print("\nPart 2 - Start")
ts = 0
tsfactors = {}

# get for each ts what buses depart then
for ts in range(len(buses)):
    if buses[ts] == 'x':
        continue

    busid = int(buses[ts])

    # fill and backfill
    alt_ts = ts
    while alt_ts >= 0:
        if alt_ts in tsfactors:
            tsfactors[alt_ts].append(busid)
        else:
            tsfactors[alt_ts] = [busid]
        alt_ts -= busid

    # future fill
    while alt_ts <= len(buses):
        alt_ts += busid
        if alt_ts in tsfactors:
            if busid not in tsfactors[alt_ts]:
                tsfactors[alt_ts].append(busid)
        else:
            tsfactors[alt_ts] = [busid]


# reduce, only keep values within larger lists
for bus in busdict:
    largest_set = 0

    # get the largest set this bus belongs in
    for day in tsfactors:
        if bus in tsfactors[day] and len(tsfactors[day]) > largest_set:
            largest_set = len(tsfactors[day])

    # remove from all other sets
    for day in tsfactors:
        if bus in tsfactors[day] and len(tsfactors[day]) < largest_set:
            tsfactors[day].remove(bus)

busgroups = {}
for day in tsfactors:
    if len(tsfactors[day]) > 0:
        busgroups[day] = tsfactors[day]

# busgroups has what I need
print("TS groups:")
print(busgroups)

# helper test function
def testn(ts, display=False):
    result = True

    if display:
        # print headings
        print("time        ", end='')
        for busid in busdict:
            print("bus " + str(busid) + " "*(5 - len(str(busid))), end='')
        print()

    for bus in buses:
        if display:
            # print ts
            print(str(ts) + ' '*(10 - len(str(ts))), end='')

        # check if it should and does depart now
        for busid in busdict:
            if bus != 'x' and ts%busid == 0:
                if display:
                    print('    D    ', end='')
            elif bus != 'x' and int(bus) == busid:
                if display:
                    print('    F    ', end='')
                result = False
            else:
                if display:
                    print('    .    ', end='')
        # end of line
        if display:
            print()

        ts += 1

    return result

# get group products
bgprod = {}
for bg in busgroups:
    prod = 1
    for num in busgroups[bg]:
        prod *= num
    bgprod[bg] = prod

print("ts group products:", bgprod)

# Automation
testy = 0
n = 0
ndigits = 0
while True:
    testy += 1
    kfg, ksg = bgprod.keys()
    pfg, psg = bgprod.values()

    # solve half eqn
    n = pfg * testy - kfg

    # check if other half can match
    testx = (n + ksg)/psg
    if int(testx) == testx:
        if testn(n):
            print("Success! n=" + str(n))
            break

