"""Aoc 2024 - Day 5."""

# import numpy as np
# import re

input_file = "input0"
input_file = "input"

# get the info
rules = []
updates = []
rules_section = True
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            rules_section = False
            continue

        if rules_section:
            rules.append(list(map(int, line.split("|"))))
        else:
            updates.append(list(map(int, line.split(","))))

# solving
good_updates = 0
mid_sum = 0
for u in updates:
    rule_failures = 0
    for r in rules:
        # testing condition for failure
        if r[0] in u and r[1] in u and u.index(r[0]) > u.index(r[1]):
            rule_failures += 1

    if rule_failures == 0:
        # get middle page
        mid_sum += u[int(len(u) / 2)]
        good_updates += 1

print("Good updates:", good_updates)

print("#### Part 1 ####")
print("Answer is:", mid_sum)


# PART 2 ####
print("============ Part 2 start ================")

fixed_mid_sum = 0
for u in updates:
    rule_failures = 0
    # find the bad updates
    for r in rules:
        # testing condition for failure
        if r[0] in u and r[1] in u and u.index(r[0]) > u.index(r[1]):
            rule_failures += 1

    # resolve them
    if rule_failures > 0:
        # fix the ordering
        # try the infinite swap technique
        # print(u)
        while True:
            rule_failures = 0
            # make swaps and check if we now pass the test
            # otherwise continue swapping
            for r in rules:
                if r[0] in u and r[1] in u and u.index(r[0]) > u.index(r[1]):
                    u[u.index(r[0])] = r[1]
                    u[u.index(r[1])] = r[0]
                    # print('swapped', r[1], r[0])
                    rule_failures += 1
            if rule_failures == 0:
                break
        # print(u)

        # get middle page
        fixed_mid_sum += u[int(len(u) / 2)]

print("#### Part 2 ####")
print("Answer is:", fixed_mid_sum)
