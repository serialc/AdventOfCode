"""AoC 2015 - Day 22."""

import cmcaoc as cmc
import copy

# import numpy as np
# import re
# import json
# import functools  # for memoization


spells = {
    "Magic Missile": {"mana": 53, "dmg": 4},
    "Drain": {"mana": 73, "dmg": 2, "heal": 2},
    "Shield": {"mana": 113, "dur": 6, "armor": 7, "effects": "hero"},
    "Poison": {"mana": 173, "dur": 6, "dmg": 3, "effects": "boss"},
    "Recharge": {"mana": 229, "dur": 5, "gain": 101, "effects": "hero"},
}


def processEffects(hero, boss, effects):
    """Make changes to target according to effect."""
    purge_effects = []

    for effect_name in effects:
        effect = effects[effect_name]

        # decrement duration of effect
        if "dur" in effect:
            effect["dur"] -= 1

        cmc.cprint("yellow", "- " + effect_name + " timer is now " + str(effect["dur"]))

        # if negative, add effect to purge list
        if effect["dur"] == 0:
            cmc.cprint("yellow", "- " + effect_name + " has ended.")
            purge_effects.append(effect_name)

        # Shield
        if effect_name == "Shield":
            if effect["dur"] == 0:
                hero["armor"] -= effect["armor"]
                cmc.cprint(
                    "orange",
                    "Hero's Shield wears off, decreasing armor by "
                    + str(effect["armor"])
                    + ".",
                )

        # Recharge
        if effect_name == "Recharge":
            hero["mana"] += effect["gain"]
            cmc.cprint("orange", "Hero recharges " + str(effect["gain"]) + " mana.")

        # Poison
        if effect_name == "Poison":
            boss["health"] -= effect["dmg"]
            cmc.cprint(
                "orange", "Boss suffers " + str(effect["dmg"]) + " poison damage."
            )

    for peff in purge_effects:
        del effects[peff]


def castSpell(hero, boss, spell_name):
    """Return mana cost and apply spell changes to target and potentially caster."""
    spell = spells[spell_name]

    # reduce caster mana
    hero["mana"] -= spell["mana"]

    # apply spell effects
    if spell_name == "Shield":
        if hero["armor"] != 0:
            exit("Unexpected armor level")
        hero["armor"] += spell["armor"]

    if spell_name == "Magic Missile":
        boss["health"] -= spell["dmg"]
        cmc.cprint(
            "orange", "Boss suffers " + str(spell["dmg"]) + " Magic Missile damage."
        )

    if spell_name == "Drain":
        hero["health"] += spell["heal"]
        boss["health"] -= spell["dmg"]
        cmc.cprint("orange", "Boss suffers " + str(spell["dmg"]) + " Drain damage.")

    return spell["mana"]


def isAlive(subject):
    """Returns boolean of whether the subject is alive."""
    if subject["health"] > 0:
        return True
    return False


def printStatus(hero, boss):
    """Display the hero and boss attributes."""
    cmc.cprint(
        "cyan",
        "Hero has "
        + str(hero["health"])
        + " hit points, "
        + str(hero["armor"])
        + " armor, "
        + str(hero["mana"])
        + " mana.",
    )
    cmc.cprint("cyan", "Boss has " + str(boss["health"]) + " hit points")


def spellSet(set_size, spell_set=[], d=0):
    """Generator returns all spell combinations of defined length."""
    if set_size == d:
        yield spell_set
        return

    for sp_name, sp_attr in spells.items():

        # skip spells with duration effects already active
        if sp_name in ["Poison", "Shield"]:
            # can't have same spell in last three spell_set items
            lb = len(spell_set) - 2
            lb = 0 if lb < 0 else lb
            if sp_name in spell_set[lb:]:
                continue

        if sp_name in ["Recharge"]:
            # can't have same spell in last two spell_set items
            lb = len(spell_set) - 2
            lb = 0 if lb < 0 else lb
            if sp_name in spell_set[lb:]:
                continue

        yield from spellSet(set_size, spell_set + [sp_name], d + 1)


def fight(wiz, oni, spell_set, lowest_mana_solution, hard_mode):
    """Solve fight and return mana usage if hero wins."""
    effect_spells = ["Recharge", "Poison", "Shield"]

    mana_cost = 0
    effects = {}

    cmc.cprint("magenta", "\n\nSTART OF FIGHT")

    # start the fight
    for i in range(len(spell_set)):
        spell = spell_set[i]

        # HERO START OF TURN
        cmc.cprint("", "🧙 turn " + str(i))
        printStatus(wiz, oni)

        if hard_mode:
            wiz["health"] -= 1
            cmc.cprint("yellow", "Hard mode. Hero suffers 1 damage.")

            if not isAlive(wiz):
                cmc.cprint("red", "Hero has died!")
                return

        # process effects
        processEffects(wiz, oni, effects)

        # check we have enough mana to cast the spell
        if wiz["mana"] < spells[spell]["mana"]:
            cmc.cprint("orange", "Fail. Insufficient mana to cast " + spell + ".")
            return

        # check the spell isn't already active
        if spell in effect_spells and spell in effects:
            cmc.cprint("orange", "Fail. Spell already in effect.")
            return

        cmc.cprint("blue", "Hero casts " + spell)
        mana_cost += castSpell(wiz, oni, spell)

        # quit if we're doing worse than best solution
        if lowest_mana_solution is not None and mana_cost > lowest_mana_solution:
            cmc.cprint(
                "orange", "Abandon. Mana use already exceeds best solution found."
            )
            return

        # add spell copy to effects
        if spell in effect_spells:
            effects[spell] = spells[spell].copy()

        # boss may have died
        if not isAlive(oni):
            cmc.cprint("green", "Boss has been killed!")
            return mana_cost
        # HERO END OF TURN

        # BOSS START OF TURN
        cmc.cprint("", "👹 turn")
        printStatus(wiz, oni)

        # process effects
        processEffects(wiz, oni, effects)

        # check if boss is still alive to attack hero
        if not isAlive(oni):
            cmc.cprint("green", "Boss has been killed!")
            return mana_cost

        # boss attacks
        wiz_dmg = oni["dmg"] - wiz["armor"]
        wiz_dmg = 1 if wiz_dmg < 1 else wiz_dmg
        wiz["health"] -= wiz_dmg
        cmc.cprint("yellow", "Boss attacks. Hero suffers " + str(wiz_dmg) + " damage.")

        if not isAlive(wiz):
            cmc.cprint("red", "Hero has died!")
            return
        # BOSS END OF TURN


def adventure(hero, boss, spells_count, lms=None, hard_mode=False):
    """Try all possible fight permutations."""
    lowest_mana_solution = lms

    successes = []

    # Provides a unique set of spell combinations (just names)
    for spell_set in spellSet(spells_count):

        # use copy of hero and boss for each fight
        result = fight(
            hero.copy(), boss.copy(), spell_set, lowest_mana_solution, hard_mode
        )

        # save result if better than previous fight
        if type(result) is int:

            # input("Observe victory above. Hit [Enter] to continue.")
            # save victories
            successes.append([spell_set, result])

            if lowest_mana_solution is None or result < lowest_mana_solution:
                lowest_mana_solution = result

    print(successes)
    return lowest_mana_solution


def tests():
    """Run some tests."""
    hero = {"health": 10, "armor": 0, "mana": 250}
    boss = {"health": 13, "dmg": 8}
    assert adventure(hero, boss, 2) == (173 + 53)
    cmc.cprint("green", "Test 1 passed")

    hero = {"health": 10, "armor": 0, "mana": 250}
    boss = {"health": 14, "dmg": 8}
    assert adventure(hero, boss, 5) == (229 + 113 + 73 + 173 + 53)
    cmc.cprint("green", "Test 2 passed")

    hero = {"health": 10, "armor": 0, "mana": 250}
    boss = {"health": 14, "dmg": 8}
    assert fight(
        hero,
        boss,
        ["Recharge", "Shield", "Drain", "Poison", "Magic Missile"],
        None,
        False,
    ) == (229 + 113 + 73 + 173 + 53)

    cmc.cprint("green", "Test 3 passed")
    print("All tests passed!")


def part1():
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = adventure(
        {"health": 50, "armor": 0, "mana": 500, "effects": []},
        # puzzle input below
        {"health": 55, "dmg": 8, "effects": []},
        9,
    )
    print("Part 1 answer is:", answer)


def part2():
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")

    # puzzle input
    hero = {"health": 50, "armor": 0, "mana": 500}
    boss = {"health": 55, "dmg": 8}

    answer = adventure(hero, boss, 9, 1295, True)

    print("Part 2 answer is:", answer)


def manual():
    """Manually try some fights to see if they work in my code."""
    wc = [
        "Poison",
        "Recharge",
        "Shield",
        "Poison",
        "Recharge",
        "Drain",
        "Poison",
        "Drain",
        "Magic Missile",
    ]

    for spells in spellSet(9):
        # check spells
        all_good = True
        for i in range(len(spells)):
            if spells[i] != wc[i]:
                all_good = False

        if all_good:
            print("Found the spell set!", spells)

    hero = {"health": 50, "armor": 0, "mana": 500}
    # puzzle input below
    boss = {"health": 55, "dmg": 8}
    score = fight(
        hero,
        boss,
        wc,
        None,
        True,
    )
    print("Score", score)


if __name__ == "__main__":
    # tests()
    # part1()
    part2()
    # manual()
