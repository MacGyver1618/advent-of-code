import copy

from common.advent_lib import *
from collections import Counter, defaultdict, deque
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

lines = full_input(24)

immune, infection = re.split(r"(?<=\n)\n", lines)
id = 0


def parse_unit(line):
    global id
    id += 1
    units, hp, damage, init = map(int, re.findall(r"\d+", line))
    dmg_type = re.search(r"does \d+ ([a-z]+) damage", line).group(1)
    weaknesses = re.search(r"(?<=weak to )([a-z, ]+)+", line)
    weaknesses = weaknesses.group(1).split(", ") if weaknesses else []
    immunities = re.search(r"(?<=immune to )([a-z, ]+)+", line)
    immunities = immunities.group(1).split(", ") if immunities else []
    return (id, units, hp, tuple(weaknesses), tuple(immunities), damage, dmg_type, init, 0)


PARTY, ID, UNITS, HP, WEAKNESSES, IMMUNITIES, DAMAGE, DAMAGE_TYPE, INITIATIVE, TURNS = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

immune = [*map(parse_unit, immune.split("\n")[1:-1])]
immune = [("immune", *unit) for unit in immune]
infection = [*map(parse_unit, infection.split("\n")[1:-1])]
infection = [("infection", *unit) for unit in infection]
original_units = [*immune, *infection]


def effective_power(unit):
    return unit[DAMAGE] * unit[UNITS]


def damage_done(attacker, defender):
    if attacker[DAMAGE_TYPE] in defender[IMMUNITIES]:
        return 0
    coeff = 2 if attacker[DAMAGE_TYPE] in defender[WEAKNESSES] else 1
    return coeff * attacker[DAMAGE] * attacker[UNITS]

def play_game(units):
    turns = 0
    while len({unit[0] for unit in units}) > 1:
        targets = dict()
        # target selection
        for current_unit in sorted(units, key=lambda unit: (-effective_power(unit),-unit[INITIATIVE])):
            enemies = [unit for unit in units if unit[PARTY] != current_unit[PARTY]]
            available_targets = [*sorted([enemy for enemy in enemies if damage_done(current_unit, enemy) > 0 and enemy[ID] not in targets.values()],
                                         key=lambda enemy: (-damage_done(current_unit, enemy),
                                                            -effective_power(enemy),
                                                            -enemy[INITIATIVE]))]
            if available_targets:
                targets[current_unit[ID]] = available_targets[0][ID]
        if not targets:
            return "draw",-1
        while [unit for unit in units if unit[TURNS] == turns]:
            current_unit = [*sorted([unit for unit in units if unit[TURNS] == turns], key=lambda unit: -unit[INITIATIVE])][0]
            if current_unit[ID] in targets:
                target_id = targets[current_unit[ID]]
                target = [unit for unit in units if unit[ID]==target_id]
                if target:
                    target = target[0]
                    dealt_damage = damage_done(current_unit, target)
                    units_killed = dealt_damage // target[HP]
                    other_units = [unit for unit in units if unit[ID] != target[ID]]
                    if units_killed < target[UNITS]:
                        target = list(target)
                        target[UNITS] -= units_killed
                        other_units += [tuple(target)]
                    units = other_units
            units = [(*current_unit[:-1], current_unit[TURNS] + 1), *[unit for unit in units if unit[ID] != current_unit[ID]]]

        turns += 1
    return units[0][PARTY] if len({unit[0] for unit in units}) == 1 else "draw", sum(unit[UNITS] for unit in units)

part1 = play_game(copy.deepcopy(original_units))[1]
print("Part 1:", part1)

def boost_unit(unit,boost):
    *rest,dmg,dtype,init,turns=unit
    return *rest,dmg+boost,dtype,init,turns

boost = 1
while True:
    boosted_immune=[*[boost_unit(unit,boost) for unit in copy.deepcopy(immune)], *copy.deepcopy(infection)]
    winner,points= play_game(boosted_immune)
    if winner == 'immune':
        part2 = points
        break
    boost += 1

print("Part 2:", part2)
