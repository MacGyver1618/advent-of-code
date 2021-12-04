from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

weapons = [
    # Weapons:      Cost   Damage   Armor
    ("Dagger",        8,     4,       0),
    ("Shortsword",   10,     5,       0),
    ("Warhammer",    25,     6,       0),
    ("Longsword",    40,     7,       0),
    ("Greataxe",     74,     8,       0)
]

armors = [
    # Armor:        Cost   Damage   Armor
    ("Nothing",       0,     0,       0),
    ("Leather",      13,     0,       1),
    ("Chainmail",    31,     0,       2),
    ("Splintmail",   53,     0,       3),
    ("Bandedmail",   75,     0,       4),
    ("Platemail",   102,     0,       5)
]

rings = [
    # Rings:        Cost   Damage   Armor
    ("Nothing",       0,     0,       0),
    ("Damage +1",    25,     1,       0),
    ("Damage +2",    50,     2,       0),
    ("Damage +3",   100,     3,       0),
    ("Defense +1",   20,     0,       1),
    ("Defense +2",   40,     0,       2),
    ("Defense +3",   80,     0,       3)
]

inpt = lines(21)
hp = int(inpt[0].split(": ")[1])
dm = int(inpt[1].split(": ")[1])
ar = int(inpt[2].split(": ")[1])

loadouts = set(map(frozenset, it.product(weapons, armors, rings, rings)))

def total_cost(loadout):
    return sum([cost for _,cost,_,_ in loadout])

player_win = 1
boss_win = 2

def play_game(loadout):
    cost = sum([c for _, c, _, _ in loadout])
    ph,pd,pa = 100, *[sum(x) for i,x in enumerate(zip(*loadout)) if i > 1]
    bh, bd, ba = 104, 8, 1
    player_turn = True
    while ph > 0 and bh > 0:
        if player_turn:
            bh -= max(pd-ba, 1)
        else:
            ph -= max(bd-pa, 1)
        player_turn = not player_turn
    if ph > 0:
        return player_win,cost
    else:
        return boss_win,cost

part1 = min([cost for outcome, cost in map(play_game, loadouts) if outcome == player_win])
print("Part 1:", part1)

part2 = max([cost for outcome, cost in map(play_game, loadouts) if outcome == boss_win])
print("Part 2:", part2)
