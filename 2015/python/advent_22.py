from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

player_turn = 1
boss_turn = 2

hard = False

def children(state):
    turn, hp, boss_hp, mana, shield_timer, poison_timer, recharge_timer, mana_spent = state
    if hp <= 0 or boss_hp <= 0:
        return
    shield_timer = max(shield_timer-1, 0)
    armor = 7 if shield_timer > 0 else 0
    if poison_timer > 0:
        boss_hp -= 3
        poison_timer -= 1
    if recharge_timer > 0:
        mana += 101
        recharge_timer -= 1
    if turn == player_turn:
        if hard:
            hp -= 1
        # Magic missile
        if mana >= 53:
            yield boss_turn, hp, boss_hp-4, mana-53, shield_timer, poison_timer, recharge_timer, mana_spent + 53
        # Drain
        if mana >= 73:
            yield boss_turn, hp+2, boss_hp-2, mana-73, shield_timer, poison_timer, recharge_timer, mana_spent + 73
        # Shield
        if mana >= 113 and shield_timer == 0:
            yield boss_turn, hp, boss_hp, mana-113, 6, poison_timer, recharge_timer, mana_spent + 113
        # Poison
        if mana >= 173 and poison_timer == 0:
            yield boss_turn, hp, boss_hp, mana-173, shield_timer, 6, recharge_timer, mana_spent + 173
        # Recharge
        if mana >= 229 and recharge_timer == 0:
            yield boss_turn, hp, boss_hp, mana-229, shield_timer, poison_timer, 5, mana_spent + 229
        # No mana
            yield boss_turn, 0, boss_hp, mana, shield_timer, poison_timer, recharge_timer, mana_spent
    else:
        yield player_turn, hp - max(9 - armor, 1), boss_hp, mana, shield_timer, poison_timer, recharge_timer, mana_spent


def play():
    Q = coll.deque()
    seen = set()
    Q.append((player_turn, 50, 58, 500, 0, 0, 0, 0))
    while Q:
        v = Q.popleft()
        if v[2] <= 0:
            yield v[-1]
        for w in children(v):
            if w not in seen:
                seen.add(w)
                Q.append(w)


print("Part 1:", min([*play()]))

hard = True
print("Part 2:", min([*play()]))
