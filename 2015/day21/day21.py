"""AoC 2015 - Day 21."""

import re

# import json
# import numpy as np
# import cmcaoc as cmc
# import functools  # for memoization


def loadInput(input_file):
    """Return input data."""
    data = {}
    with open(input_file, "r") as fh:
        mode = None
        for line in fh:
            line = line.strip("\n")

            if line == "":
                continue

            if ":" in line:
                mode = line.split(":")[0]
                data[mode] = []
                continue

            if mode == "Rings":
                rem = re.match(r"(\w+) \+\d +(\d+) +(\d+) +(\d+)", line)
            else:
                rem = re.match(r"(\w+) +(\d+) +(\d+) +(\d+)", line)

            iname, cost, dmg, armor = rem.groups()
            data[mode].append(
                {"name": iname, "cost": int(cost), "dmg": int(dmg), "armor": int(armor)}
            )
    return data


def fight(hero, boss):
    """Returns whether the hero won the fight."""
    while True:
        # print("Hero:", hero["health"], "Boss:", boss["health"])
        # hero attacks
        hadmg = hero["dmg"] - boss["armor"]
        hadmg = hadmg if hadmg > 0 else 1
        boss["health"] -= hadmg

        if boss["health"] <= 0:
            return True

        # boss attacks
        badmg = boss["dmg"] - hero["armor"]
        badmg = badmg if badmg > 0 else 1
        hero["health"] -= badmg

        if hero["health"] <= 0:
            return False


def shop(store, kit=[], stage=0):
    """Recursively return all store purchase permutations."""
    if stage == 3:
        return [kit]

    kitlist = []
    # Select one weapon
    if stage == 0:
        for wi in range(len(store["Weapons"])):
            kitlist += shop(store, [store["Weapons"][wi]], 1)

    # Select 0-1 armor
    if stage == 1:
        kitlist += shop(store, kit.copy(), 2)
        for ai in range(len(store["Armor"])):
            kitlist += shop(store, kit.copy() + [store["Armor"][ai]], 2)

    # Select 0-2 rings
    if stage == 2:
        # add kit with no rings
        kitlist.append(kit)

        # add kit with one and two ring
        for ri in range(len(store["Rings"])):
            kitlist += shop(store, kit.copy() + [store["Rings"][ri]], 3)
            # don't go out of bounds
            if ri < (len(store["Rings"]) - 2):
                for r2i in range(ri + 1, len(store["Rings"])):
                    rings = [store["Rings"][ri], store["Rings"][r2i]]
                    kitlist += shop(store, kit.copy() + rings, 3)

    return kitlist


def printStore(store):
    """Display store contents."""
    for k, v in store.items():
        print(k)
        for eq in v:
            print(eq)


def adventure(store, hero, boss, p2=False):
    """Return the lowest cost successful fight against the boss."""
    # get all equipment permutations
    # printStore(store)

    mincost = None
    maxcost = None
    # go through each permutation
    for kit in shop(store):
        # print("This kit:", kit)

        # augment hero
        this_hero = hero.copy()
        # print("Hero:", this_hero)
        kitcost = 0
        for ki in kit:
            this_hero["dmg"] += ki["dmg"]
            this_hero["armor"] += ki["armor"]
            kitcost += ki["cost"]
        # print("Leveled up hero:", this_hero, "at cost", kitcost)

        # Fight with this kit equipped
        if fight(this_hero, boss.copy()):
            # print("Won fight at cost", kitcost)
            if mincost is None or kitcost < mincost:
                mincost = kitcost
        else:
            # lost
            if maxcost is None or kitcost > maxcost:
                maxcost = kitcost

    if p2:
        return maxcost
    else:
        return mincost


def tests(data):
    """Run some tests."""
    assert fight(
        {"health": 8, "dmg": 5, "armor": 5}, {"health": 12, "dmg": 7, "armor": 2}
    )
    print("All tests passed!")


def part1(data):
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = adventure(
        data,
        {"health": 100, "dmg": 0, "armor": 0},
        {"health": 109, "dmg": 8, "armor": 2},
    )
    print("Part 1 answer is:", answer)
    # 10 - wrong. I didn't pass a copy of the boss, his life carried over across battles


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    answer = adventure(
        data,
        {"health": 100, "dmg": 0, "armor": 0},
        {"health": 109, "dmg": 8, "armor": 2},
        True,
    )
    print("Part 2 answer is:", answer)


if __name__ == "__main__":
    data = loadInput("store")
    tests(data)

    part1(data)
    part2(data)
