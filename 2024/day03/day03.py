"""AoC 2024 - Day 3."""

# import numpy as np
import re

input_file = "input0"
input_file = "input"

prod = 0
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        mulmatches = re.findall(r"(mul\((\d+),(\d+)\))", line)
        for m in mulmatches:
            # print(m[0])
            if len(m[1]) > 3 or len(m[2]) > 3:
                print("Skipping! Digit too long!")
                continue

            prod += int(m[1]) * int(m[2])

print("#### Part 1 ####")
print("Answer is:", prod)
# too low - 30902624, had only looked at first line!


# PART 2 ####
print("============ Part 2 start ================")

input_file = "input1"
input_file = "input"

prod = 0
with open(input_file, "r") as fh:
    do = True
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        mulmatches = re.findall(r"(mul\((\d+),(\d+)\))|(do)\(\)|(don)\'t\(\)", line)
        for m in mulmatches:
            # print(m)
            if m[3] == "do":
                do = True
                continue

            if m[4] == "don":
                do = False
                continue

            if do:
                if len(m[1]) > 3 or len(m[2]) > 3:
                    print("Skipping! Digit too long!")
                    continue

                prod += int(m[1]) * int(m[2])

print("#### Part 2 ####")
print("Answer is:", prod)
# too high - 107516772, was resetting to 'do' at new line
