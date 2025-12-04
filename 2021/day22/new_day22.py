"""AoC 2021 day 22."""

# import numpy as np

input_file = "test_input"
# input_file = 'test_input_larger'
# input_file = 'test_input_p2'
# input_file = 'input'


def splitAfter(corei, xr, yr, zr):
    """Split core with limits."""


cores = []

with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip()

        on_or_off, xyz = line.split(" ")
        x, y, z = xyz.split(",")
        xr = [int(v) for v in x[2:].split("..")]
        yr = [int(v) for v in y[2:].split("..")]
        zr = [int(v) for v in z[2:].split("..")]

        print(on_or_off, xr, yr, zr)

        # slice all existing cores based on this instruction set's limits

        # delete all cores that fall within this  instruction

        # create a new instruction core set with these bounds
        cores.append([xr, yr, zr, on_or_off])

# PART 1 #####
# How many cubes are in the x=-50..50,y=-50..50,z=-50..50 core?
print("Part 1")
print("Final Core sum", -99)


# PART 2 #####
# Way bigger cube, can't calculate through 3D volume of cells - too big/many
print("Part 2")
