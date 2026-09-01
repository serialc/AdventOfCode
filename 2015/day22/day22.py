"""AoC 2015 - Day 22."""

import cmcaoc as cmc
import copy

# import numpy as np
# import re
# import json
# import functools  # for memoization


spells = [
    {"name": "recharge", "mana": 229, "dur": 5, "gain": 101, "effects": "hero"},
    {"name": "poison", "mana": 173, "dur": 6, "dmg": 3, "effects": "boss"},
    {"name": "shield", "mana": 113, "armor": 7, "dur": 6, "effects": "hero"},
    {"name": "drain", "mana": 73, "dmg": 2, "heal": 2},
    {"name": "magic missile", "mana": 53, "dmg": 4},
]


mana_min_win = None
ends = {"wins": 0, "deaths": 0, "no_mana": 0}
win_paths = []  # type: ignore


def spellIsActive(subjects, spell):
    """Determine if an effect spell is active for the hero or boss."""
    for subject in subjects:
        for effect in subject["effects"]:
            if effect["name"] == spell["name"]:
                return True

    return False


def castSpell(caster, target, spell):
    """Return mana cost and apply spell changes to target and potentially caster."""
    caster["mana"] -= spell["mana"]

    if spell["name"] == "magic missile":
        target["health"] -= spell["dmg"]

    if spell["name"] == "drain":
        target["health"] -= spell["dmg"]
        caster["health"] += spell["heal"]

    return spell["mana"]


def initEffect(caster, target, spell):
    """Return the mana cost and initialize the effect for the target."""
    caster["mana"] -= spell["mana"]
    target["effects"].append(spell.copy())

    # recharge and (boss) poison don't require additional initialization
    if spell["name"] == "shield":
        target["armor"] += spell["armor"]

    return spell["mana"]


def processEffect(target, effect_index):
    """Make changes to target and effect."""
    effect = target["effects"][effect_index]

    if "dur" in effect:
        effect["dur"] -= 1

    # effects that concern hero (shield, recharge)
    # Shield/armor spell
    if effect["name"] == "shield":
        if effect["dur"] == 0:
            cmc.cprint("yellow", "- Shield armor buff has ended.")
            target["armor"] -= effect["armor"]
            return False
        cmc.cprint("yellow", "- Shield's timer is now " + str(effect["dur"]))

    # Recharge spell
    if effect["name"] == "recharge":
        if effect["dur"] == 0:
            cmc.cprint("yellow", "- Mana recharge has ended.")
            return False
        cmc.cprint(
            "yellow",
            "- Mana recharged +"
            + str(effect["gain"])
            + "; timer is now "
            + str(effect["dur"])
            + ".",
        )
        target["mana"] += effect["gain"]

    # effect that concern boss (poison)
    if effect["name"] == "poison":
        if effect["dur"] == 0:
            cmc.cprint("yellow", "- Poison finished.")
            return False
        target["health"] -= effect["dmg"]
        cmc.cprint(
            "yellow",
            "- Poison damages Boss health "
            + str(effect["dmg"])
            + " hit points; its timer is now "
            + str(effect["dur"]),
        )
    return True


def applyEffects(hero, boss):
    """Apply effects present to both the hero and boss."""
    # hero effects
    del_effects = []
    for ei in range(len(hero["effects"])):
        if not processEffect(hero, ei):
            del_effects.append(ei)

    # delete any expired effects (carefully)
    del_effects.sort(reverse=True)
    for i in del_effects:
        hero["effects"].pop(i)

    # boss effects
    del_effects = []
    for ei in range(len(boss["effects"])):
        if not processEffect(boss, ei):
            del_effects.append(ei)

    # delete any expired effects (carefully)
    del_effects.sort(reverse=True)
    for i in del_effects:
        boss["effects"].pop(i)


def fight(hero, boss, turn="hero", mana_cost=0, d=0, spcast=[]):
    """Return the lowest mana solution for victory against boss."""
    global mana_min_win
    global ends
    global win_paths

    # reset the global mana_min_win and stats for new fight
    if d == 0 and turn == "hero":
        mana_min_win = 1250
        ends = {"wins": 0, "deaths": 0, "no_mana": 0, "exceeds": 0}
        win_paths = []

    # pad print statement with recursion level for debug
    pad = " " * d

    # We only check boss health here, as effect can kill him
    # Hero health is checked directly after boss attack
    if boss["health"] <= 0:
        cmc.cprint("green", pad + "Boss has died! Mana cost was " + str(mana_cost))
        ends["wins"] += 1
        win_paths.append(spcast + [str(mana_cost)])
        exit()
        return mana_cost

    # START OF HERO/BOSS TURN
    # These must be completed in entirety
    if turn == "hero":
        print(pad + " 🧙 turn")
    else:
        print(pad + " 👹 turn")

    # show hero and boss states before effects are applied
    print(
        pad
        + " Hero has "
        + str(hero["health"])
        + " hit points,"
        + str(hero["armor"])
        + " armor,"
        + str(hero["mana"])
        + " mana."
    )
    print(pad + " Boss has " + str(boss["health"]) + " hit points")

    # start with effects
    applyEffects(hero, boss)

    # Recursion branching
    if turn == "hero":
        loc_min_mana = None

        # hero attacks
        for spell in spells:
            # can't cast spells if still in effect (shield, poison, or recharge)
            if spellIsActive([hero, boss], spell):
                continue

            # prevent recursion branch if this path will yield a worse mana score
            if mana_min_win is not None and (spell["mana"] + mana_cost) > mana_min_win:
                ends["exceeds"] += 1
                continue

            no_action = True
            # does hero have enough mana to cast this spell
            if spell["mana"] <= hero["mana"]:
                cmc.cprint("cyan", pad + " Hero casts " + spell["name"])
                no_action = False

                spell_mana_cost = None
                hero_copy = copy.deepcopy(hero)
                boss_copy = copy.deepcopy(boss)

                # is it an effects spell?
                if "effects" in spell:
                    if spell["effects"] == "hero":
                        spell_mana_cost = initEffect(hero_copy, hero_copy, spell)
                    else:
                        spell_mana_cost = initEffect(hero_copy, boss_copy, spell)
                else:
                    # must be 'magic missile' or 'drain'
                    spell_mana_cost = castSpell(hero_copy, boss_copy, spell)

                # now recursion
                win_mana_cost = fight(
                    hero_copy,
                    boss_copy,
                    "boss",
                    mana_cost + spell_mana_cost,
                    d,
                    spcast.copy() + [spell["name"]],
                )

                if win_mana_cost is False:
                    continue

                # update the best local and global mana score
                if loc_min_mana is None or win_mana_cost < loc_min_mana:
                    loc_min_mana = win_mana_cost
                if mana_min_win is None or win_mana_cost < mana_min_win:
                    mana_min_win = win_mana_cost

            # it is never worthwhile taking no action, it means another path would have been better
            if no_action:
                print(pad, "No action taken")
                ends["no_mana"] += 1
                return False
        if loc_min_mana is None:
            return False
        return loc_min_mana
        # END OF HERO TURN

    if turn == "boss":
        # boss can only damage hero if still alive
        if boss["health"] > 0:
            # boss attacks - calculate damage
            boss_attack_dmg = boss["dmg"] - hero["armor"]
            boss_attack_dmg = 1 if boss_attack_dmg < 1 else boss_attack_dmg
            hero["health"] -= boss_attack_dmg

            cmc.cprint(
                "orange",
                pad
                + " Boss attacks for ("
                + str(boss["dmg"])
                + " - "
                + str(hero["armor"])
                + ") "
                + str(boss_attack_dmg)
                + " damage.",
            )

        # END OF BOSS TURN

        # Potential recursion end
        if hero["health"] <= 0:
            cmc.cprint("red", pad + " Hero has died!")
            ends["deaths"] += 1
            return False

        # boss doesn't need to create copies - he doesn't branch
        # this will always return to the hero branch
        return fight(hero, boss, "hero", mana_cost, d + 1, spcast)


def tests():
    """Run some tests."""
    assert fight(
        {"health": 10, "armor": 0, "mana": 250, "effects": []},
        {"health": 13, "dmg": 8, "effects": []},
    ) == (173 + 53)
    print("win_paths", win_paths)
    print("Summary", ends)
    cmc.cprint("green", "Test 1 passed")

    assert fight(
        {"health": 10, "armor": 0, "mana": 250, "effects": []},
        {"health": 14, "dmg": 8, "effects": []},
    ) == (229 + 113 + 73 + 173 + 53)
    print(win_paths)
    print(ends)
    cmc.cprint("green", "Test 2 passed")

    # Are we detecting correctly that effect spells are already active
    hero = {"health": 10, "armor": 0, "mana": 250, "effects": []}
    boss = {"health": 13, "dmg": 8, "effects": []}
    hero["effects"].append(spells[0])
    boss["effects"].append(spells[1])
    hero["effects"].append(spells[2])

    assert spellIsActive([hero], spells[0])
    assert spellIsActive([boss], spells[1])
    assert spellIsActive([hero], spells[2])
    print("All tests passed!")


def part1():
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = fight(
        {"health": 50, "armor": 0, "mana": 500, "effects": []},
        # puzzle input below
        {"health": 55, "dmg": 8, "effects": []},
    )
    print(answer)
    print(win_paths)
    for wp in win_paths:
        cmc.cprint("cyan", ",".join(wp))
    print("Stats", ends)
    print("Part 1 answer is:", answer)
    # 491 - too low. Problem with not removing shield effect.
    # 780 - too low. Was not removing poison effect from Boss.
    # 1249 - too high. Was losing data from first recursion... but no change.


def part2(data):
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    # turn on corner lights
    answer = main(data)
    print("Part 2 answer is:", answer)


if __name__ == "__main__":
    # tests()
    part1()
    # part2()
