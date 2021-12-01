
# build data in dict
instructions = {}
with open('input.txt','r') as fh:
    lnum = 0
    for line in fh:
        line = line.rstrip()
        cmd, value = line.split(' ')
        instructions[lnum] = [cmd, int(value)]
        lnum += 1

# Part 1
# follow instructions
lnum = 0
accu = 0
visited = []
while True:
    # if we've seen this instruction line before, break
    if lnum in visited:
        break
    visited.append(lnum)

    cmd, value = instructions[lnum]

    if cmd == 'nop':
        lnum += 1

    if cmd == 'acc':
        accu += value
        lnum += 1

    if cmd == 'jmp':
        lnum += value

print("\nPart 1: " + str(accu) + "\n")

# Part 2
# follow instructions

change_jn_instr = 1
finished = False
while True:

    print("Changing instruction " + str(change_jn_instr))

    lnum = 0
    accu = 0
    jn_instr_count = 0
    visited = []
    while True:

        # if we've seen this instruction line before, break
        if lnum in visited:
            print("Loop - fail, incrementing instruction swapper by +1")
            print("Accu sum = " + str(accu) + "\n")
            change_jn_instr += 1
            break

        # good, reached end of instructions
        if lnum == len(instructions):
            print("Success!")
            finished = True
            break

        visited.append(lnum)

        cmd, value = instructions[lnum]
        #print("This command is " + cmd + " " + str(value))

        # change command if correct instruction
        if cmd in ['nop', 'jmp']:
            #print("Swap check")
            jn_instr_count += 1

            if jn_instr_count == change_jn_instr:
                print("Swapping instruction for line " + str(lnum))
                if cmd == 'nop':
                    cmd = 'jmp'
                else:
                    cmd = 'nop'

        if cmd == 'nop':
            lnum += 1

        if cmd == 'acc':
            accu += value
            lnum += 1

        if cmd == 'jmp':
            lnum += value

    if finished is True:
        break

print("\nPart 2: " + str(accu))
