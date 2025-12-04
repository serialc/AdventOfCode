"""AoC 2024 - Day 3."""

input_file = "input0"
input_file = "input"

jsum = 0

with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        nums = [int(x) for x in list(line)]
        m1 = max(nums)
        i1 = nums.index(m1)
        del nums[i1]
        m2 = max(nums)
        i2 = nums.index(m2)

        # form i1 i2
        if i1 <= i2:
            jsum += int(str(m1) + str(m2))
            # print(str(m1) + str(m2))
            continue

        # form i1 at the end
        if i1 == (len(line) - 1):
            jsum += int(str(m2) + str(m1))
            # print(str(m2) + str(m1))
            continue

        # form i1 not at the end
        nxt = max(nums[i1:])
        jsum += int(str(m1) + str(nxt))
        # print(str(m1) + str(nxt))

print("#### Part 1 ####")
print("Answer is:", jsum)

# PART 2 ####
print("============ Part 2 start ================")


def getLargest(nums, length):
    """Find the largest digit in range."""
    digit = max(nums[: (-length + 1)])
    i = nums[: (-length + 1)].index(digit)

    length -= 1

    # end recursion when looking for the last digit
    if length == 1:
        return str(digit) + str(max(nums[(i + 1) :]))

    return str(digit) + getLargest(nums[(i + 1) :], length)


jsum = 0
with open(input_file, "r") as fh:
    for line in fh:
        line = line.strip("\n")

        if line == "":
            continue

        nums = [int(x) for x in list(line)]

        jolt = int(getLargest(nums, 12))
        # print(jolt)
        jsum += jolt

print("#### Part 2 ####")
print("Answer is:", jsum)
