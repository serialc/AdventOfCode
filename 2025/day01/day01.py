"""AoC 2024 - Day 1."""

input_file = "input0"
input_file = "input"

zerohit = 0
zeropass = 0
dial = 50
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        direction = line[0]
        clicks = int(line[1:])

        print(
            "Status: Dial-", dial % 100, "Inst-", line, "ZP-", zeropass, "ZH-", zerohit
        )

        if direction == "L":
            if (dial % 100) != 0 and (dial % 100) < (clicks % 100):
                print("Zero pass on " + line)
                zeropass += 1
            dial -= clicks
        if direction == "R":
            if (dial % 100) != 0 and (100 - (dial % 100)) < (clicks % 100):
                print("Zero pass on " + line)
                zeropass += 1
            dial += clicks

        # watch out for click spins (clicks > 100)
        spins = int(clicks / 100)
        if spins > 0:
            print("Spins:", spins)
            zeropass += spins

        # is dial pointing at 0?
        if (dial % 100) == 0:
            zerohit += 1


print("#### Part 1 ####")
print("Answer is:", zerohit)

# PART 2 ####
print("============ Part 2 start ================")

print("Zero pass:", zeropass)
# 6428 is too high - I wasn't checking the (dial % 100) value, but the dial :(
print("#### Part 2 ####")
print("Answer is:", zerohit + zeropass)
