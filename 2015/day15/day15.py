"""AoC 2015 - Day 15."""

import re

# import json
# import numpy as np
# import cmcaoc as cmc
# import functools  # for memoization

cal_limit = 500


def loadInput(input_file):
    """Return input data."""
    data = {}
    with open(input_file, "r") as fh:
        for line in fh:
            line = line.strip("\n")

            if line == "":
                continue

            if line[0] == "#":
                continue

            # Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
            res = re.match(
                r"(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)",
                line,
            )

            # extract and clean up
            ing = res.groups()[0]
            cap, dur, flv, tex, cal = [int(x) for x in res.groups()[1:]]

            data[ing] = {"cap": cap, "dur": dur, "flv": flv, "tex": tex, "cal": cal}
    return data


def getRecipeScore(data):
    """Return the recipe score."""
    cap, dur, flv, tex = 0, 0, 0, 0
    for i in data:
        ing = data[i]
        q = ing["q"]
        cap += q * ing["cap"]
        dur += q * ing["dur"]
        flv += q * ing["flv"]
        tex += q * ing["tex"]
        # print(cap, dur, flv, tex)
    return cap * dur * flv * tex


def getCalories(data):
    """Return the recipe calories."""
    cals = 0
    for i in data:
        cals += data[i]["cal"] * data[i]["q"]
    return cals


def recipe(data, calories=False):
    """Return the best recipe."""

    # initialize ingredient distribution
    portion = int(100 / len(data))

    # add a portion for each ingredient
    for i in data:
        data[i]["q"] = portion

    # add division remainder, if any, to last ingredient
    data[i]["q"] += 100 - (len(data) * portion)

    hscore = 0
    while True:
        score_tracker = hscore
        # for each ingredient, try swapping with each other ingredient one q
        for i in data:
            ing1 = data[i]
            for j in data:
                ing2 = data[j]

                # get the current score
                score0 = getRecipeScore(data)
                cal0 = getCalories(data)

                # ing2 -> ing1
                ing2["q"] -= 1
                ing1["q"] += 1
                score1 = getRecipeScore(data)
                cal1 = getCalories(data)

                # ing1 -> ing2 (offset above shift)
                ing1["q"] -= 2
                ing2["q"] += 2
                score2 = getRecipeScore(data)
                cal2 = getCalories(data)

                # evaluate calories
                if calories:
                    print("Calorie options", cal0, cal1, cal2)

                    # if current calories exceed limit
                    if cal0 > cal_limit:
                        # need to change something
                        score0 = 0

                    # if both alternatives exceed limit
                    if cal1 > cal_limit and cal2 > cal_limit:
                        # chose the lower calories of the two
                        if cal1 < cal2:
                            score2 = 0
                        if cal1 > cal2:
                            score1 = 0
                        # if equal, then below will choose higher score of two

                    # if both are below limit
                    elif cal1 <= cal_limit and cal2 <= cal_limit:
                        # do nothing, below will choose higher score of two
                        pass

                    # only one is below the limit
                    else:
                        if cal1 < cal2:
                            score2 = 0
                        else:
                            score1 = 0

                # revert ingredient portions to highest score and update hscore
                if score0 >= score1 and score0 >= score2:
                    # back to initial condition
                    ing2["q"] -= 1
                    ing1["q"] += 1
                    print("Before was better")
                else:
                    if score1 > score2:
                        # increase ingredient 1 by 1 amount
                        ing2["q"] -= 2
                        ing1["q"] += 2
                        print("More", i, "is better")
                        hscore = score1
                    else:
                        # already portioned correctly
                        print("More", j, "is better")
                        hscore = score2

                print("Selected calories", getCalories(data))
        # if we see no change, reached optimum, break
        if hscore == score_tracker:
            break
    print("Calories", getCalories(data))
    return hscore


def tests(data):
    """Run some tests."""
    assert recipe(data) == 62842880
    assert recipe(data, True) == 57600000
    print("All tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = recipe(data)
    print("Part 1 answer is:", answer)


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    answer = recipe(data, True)
    print("Part 2 answer is:", answer)
    # 2303000 - Too high: Would sometimes accept over caloried option.


if __name__ == "__main__":
    tdata = loadInput("input0")
    tests(tdata)

    data = loadInput("input")
    part1(data)
    part2(data)
