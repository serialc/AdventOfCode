import re
import numpy as np

input_file = 'input_test.txt'
input_file = 'input_test2.txt'
input_file = 'input.txt'

def solve(eqn):
    print("Solve ", eqn)
    parts = []
    ops= []
    parsearch = False
    parlvl = 0
    ipar = 0

    # need to break into bits
    while True:
        if parsearch:
            #print("Search", ipar, eqn[ipar])
            if eqn[ipar] == '(':
                parlvl += 1
            elif eqn[ipar] == ')':
                parlvl -= 1

            if parlvl == 0:
                eqn = str(solve(eqn[1:ipar])) + eqn[ipar+1:]
                print("Updated equation", eqn)
                parsearch = False
                ipar = 0
                continue
            
            ipar += 1
            continue

        if len(eqn) > 0 and eqn[0] == '(':
            parsearch = True
            parlvl += 1
            ipar += 1
            continue

        digfirst = re.match("(\d+) ([\*\+])(.*)", eqn)
        if digfirst:
            dig = int(digfirst.groups()[0])
            op  = digfirst.groups()[1]
            eqn  = digfirst.groups()[2].lstrip()

            parts.append(dig)
            ops.append(op)
            continue

        traildig = re.match("(\d+)(.*)", eqn)
        if traildig:
            dig = int(traildig.groups()[0])
            eqn = traildig.groups()[1].lstrip()

            parts.append(dig)
            continue
        
    
        #print("Finished parsing equation")
        break

    # Now start adding or multiplying
    #print(parts, ops)

    # Part 1
    while len(ops) > 0:
        if '+' in ops:
            for opi in range(len(ops)):
                if ops[opi] == '+':
                    parts.insert(opi, parts.pop(opi) + parts.pop(opi))
                    ops.pop(opi)
                    print(parts, ops)
                    break
            continue

        op = ops.pop(0)

        if op == '+':
            print("ERROR - This shouldn't occur")
        if op == '*':
            parts.insert(0, parts.pop(0) * parts.pop(0))


    #print(parts, ops)
    # last part in parts is the solved value
    print("Solved to", parts[0])
    return parts[0]



eqns_sum = 0
with open(input_file, 'r') as fh:
    ypos = None
    for line in fh:
        line = line.rstrip()
        eqn = line
        eqns_sum += solve(eqn)

print("Part 1 - Sum of all equations", eqns_sum)
