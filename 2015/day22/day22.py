"""AoC 2015 - Day 22."""

import cmcaoc as cmc
import copy

# import numpy as np
# import re
# import json
# import functools  # for memoization


spells = [
    {"name": "magic missile", "mana": 53, "dmg": 4},
    {"name": "drain", "mana": 73, "dmg": 2, "heal": 2},
    {"name": "shield", "mana": 113, "armor": 7, "dur": 6, "effects": "hero"},
    {"name": "poison", "mana": 173, "dur": 6, "dmg": 3, "effects": "boss"},
    {"name": "recharge", "mana": 229, "dur": 5, "gain": 101, "effects": "hero"},
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
        if effect["dur"] < 0:
            cmc.cprint("yellow", "- Shield armor buff has ended.")
            target["armor"] -= effect["armor"]
            return False
        cmc.cprint("yellow", "- Shield's timer is now " + str(effect["dur"]))

    # Recharge spell
    if effect["name"] == "recharge":
        if effect["dur"] < 0:
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
        if effect["dur"] < 0:
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


def fight(hero, boss, hard_mode=False, turn="hero", mana_cost=0, d=0, spcast=[]):
    """Return the lowest mana solution for victory against boss."""
    global mana_min_win
    global ends
    global win_paths

    # reset the global mana_min_win and stats for new fight
    if d == 0 and turn == "hero":
        mana_min_win = 1295
        ends = {"wins": 0, "deaths": 0, "no_mana": 0, "exceeds": 0}
        win_paths = []

    # pad print statement with recursion level for debug
    pad = " " * d

    # We only check boss health here, as effect can kill him
    # Hero health is checked directly after boss attack
    if boss["health"] <= 0:
        cmc.cprint("green", pad + "Boss has died! Mana cost was " + str(mana_cost))
        cmc.cprint("cyan", ",".join(spcast))
        ends["wins"] += 1
        win_paths.append(spcast + [str(mana_cost)])
        return mana_cost

    # START OF HERO/BOSS TURNS
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

    # Hard mode
    if turn == "hero" and hard_mode:
        hero["health"] -= 1
        print(pad + " Hard mode: Hero health decreased by 1 to", hero["health"])
        if hero["health"] <= 0:
            cmc.cprint("red", pad + " Hard mode killed the hero!")
            return False

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
                        # hero casts on himself
                        spell_mana_cost = initEffect(hero_copy, hero_copy, spell)
                    else:
                        # hero casts on boss
                        spell_mana_cost = initEffect(hero_copy, boss_copy, spell)
                else:
                    # must be 'magic missile' or 'drain'
                    spell_mana_cost = castSpell(hero_copy, boss_copy, spell)

                # now recursion
                win_mana_cost = fight(
                    hero_copy,
                    boss_copy,
                    hard_mode,
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
        return fight(hero, boss, hard_mode, "hero", mana_cost, d + 1, spcast)


def tests():
    """Run some tests."""
    hero = {"health": 10, "armor": 0, "mana": 250, "effects": []}
    boss = {"health": 13, "dmg": 8, "effects": []}
    assert fight(copy.deepcopy(hero), copy.deepcopy(boss)) == (173 + 53)
    print("win_paths", win_paths)
    print("Summary", ends)
    cmc.cprint("green", "Test 1 passed")

    boss = {"health": 14, "dmg": 8, "effects": []}
    assert fight(copy.deepcopy(hero), copy.deepcopy(boss)) == (
        229 + 113 + 73 + 173 + 53
    )
    print(win_paths)
    print(ends)
    cmc.cprint("green", "Test 2 passed")

    # Are we detecting correctly that effect spells are already active
    hero = {"health": 10, "armor": 0, "mana": 515, "effects": []}
    boss = {"health": 13, "dmg": 8, "effects": []}
    initEffect(hero, hero, spells[2])
    initEffect(hero, boss, spells[3])
    initEffect(hero, hero, spells[4])

    assert spellIsActive([hero], spells[2])
    assert spellIsActive([boss], spells[3])
    assert spellIsActive([hero], spells[4])

    applyEffects(hero, boss)
    assert hero["armor"] == 7
    assert boss["health"] == 10
    assert hero["mana"] == 101
    applyEffects(hero, boss)
    assert hero["armor"] == 7
    assert boss["health"] == 7
    assert hero["mana"] == 202
    applyEffects(hero, boss)
    assert hero["armor"] == 7
    assert boss["health"] == 4
    assert hero["mana"] == 303
    applyEffects(hero, boss)
    assert hero["armor"] == 7
    assert boss["health"] == 1
    assert hero["mana"] == 404
    applyEffects(hero, boss)
    assert hero["armor"] == 7
    assert boss["health"] == -2
    assert hero["mana"] == 505
    applyEffects(hero, boss)
    assert hero["armor"] == 7
    assert boss["health"] == -5
    assert hero["mana"] == 505
    applyEffects(hero, boss)
    assert hero["armor"] == 0
    assert boss["health"] == -5
    assert hero["mana"] == 505

    hero = {"health": 11, "armor": 0, "mana": 250, "effects": []}
    boss = {"health": 13, "dmg": 8, "effects": []}
    assert fight(copy.deepcopy(hero), copy.deepcopy(boss), True) == (173 + 53)

    hero = {"health": 15, "armor": 0, "mana": 250, "effects": []}
    boss = {"health": 14, "dmg": 8, "effects": []}
    assert fight(copy.deepcopy(hero), copy.deepcopy(boss), True) == (
        229 + 113 + 73 + 173 + 53
    )
    print("All tests passed!")


def part1():
    """Solves and prints part1 answer."""
    print("#### Part 1 ####")
    answer = fight(
        {"health": 50, "armor": 0, "mana": 500, "effects": []},
        # puzzle input below
        {"health": 55, "dmg": 8, "effects": []},
    )
    print(win_paths)
    for wp in win_paths:
        cmc.cprint("cyan", ",".join(wp))
    print("Stats", ends)
    print("Part 1 answer is:", answer)
    # 491 - too low. Problem with not removing shield effect.
    # 780 - too low. Was not removing poison effect from Boss.
    # 1249 - too high. Decrement of turns went too fast by 1. (e.g. recharge lasted 4 rather than 5 turns)


def part2():
    """Solves and prints part2 answer."""
    print("#### Part 2 ####")
    # turn on corner lights
    answer = fight(
        {"health": 50, "armor": 0, "mana": 500, "effects": []},
        # puzzle input below
        {"health": 55, "dmg": 8, "effects": []},
        True,
    )
    print(win_paths)
    for wp in win_paths:
        cmc.cprint("cyan", ",".join(wp))
    print("Stats", ends)
    print("Part 2 answer is:", answer)
    # 1295 - too high.


if __name__ == "__main__":
    # tests()
    # part1()
    part2()
