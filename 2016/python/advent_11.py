from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(11)

elevator = {"E"}
gens = {"SG", "PG", "TG", "RG", "CG"}
chips = {"SM", "PM", "TM", "RM", "CM"}
pairs = {frozenset({"SG", "SM"}),
         frozenset({"PG", "PM"}),
         frozenset({"TG", "TM"}),
         frozenset({"CG", "CM"}),
         frozenset({"RG", "RM"})}

init = (
    frozenset({"E", "SG", "SM", "PG", "PM"}),
    frozenset({"TG", "RG", "RM", "CG", "CM"}),
    frozenset({"TM"}),
    frozenset({})
)

target = (
    frozenset({}),
    frozenset({}),
    frozenset({}),
    frozenset(union(init))
)

def is_unsafe(floor: set):
    unpaired: set = func.reduce(set.difference, filter(floor.issuperset, map(set, pairs)), set(floor))
    return floor.intersection(gens) and unpaired.intersection(chips)

def is_valid(state: tuple[set]):
    return not [*filter(is_unsafe, state)]

def has_elevator(floor: set):
    return floor.intersection(elevator)

Q = coll.deque()
seen = set()
came_from = {}
Q.append(init)


def adjacent(v):
    for i, floor in enumerate(v):
        if has_elevator(floor):
            size_2 = set(filter(has_elevator, map(frozenset, it.combinations(floor, 2))))
            size_3 = set(filter(has_elevator, map(frozenset, it.combinations(floor, 3))))
            moves = frozenset(union((size_2, size_3)))
            for move in moves:
                if i - 1 >= 0:
                    new_state = list(v).copy()
                    new_state[i-1] = frozenset(union((new_state[i-1], move)))
                    new_state[i] = frozenset(new_state[i].difference(move))
                    if is_valid(new_state):
                        yield tuple(new_state)
                if i + 1 < 4:
                    new_state = list(v).copy()
                    new_state[i+1] = frozenset(union((new_state[i+1], move)))
                    new_state[i] = frozenset(new_state[i].difference(move))
                    if is_valid(new_state):
                        yield tuple(new_state)

def construct_path(v):
    cur = v
    l = 0
    while cur in came_from:
        l += 1
        cur = came_from[cur]
    return l

while Q:
    v = Q.popleft()
    if v == target:
        part1 = construct_path(v)
        break
    if v not in seen:
        seen.add(v)
        for n in adjacent(v):
            if n not in seen:
                Q.append(n)
                came_from[n] = v

print("Part 1:", part1)



elevator = {"E"}
gens = {"SG", "PG", "TG", "RG", "CG", "EG", "DG"}
chips = {"SM", "PM", "TM", "RM", "CM", "EM", "DM"}
pairs = {frozenset({"SG", "SM"}),
         frozenset({"PG", "PM"}),
         frozenset({"TG", "TM"}),
         frozenset({"CG", "CM"}),
         frozenset({"DG", "DM"}),
         frozenset({"EG", "EM"}),
         frozenset({"RG", "RM"})}

init = (
    frozenset({"E", "SG", "SM", "PG", "PM", "EG", "EM", "DG", "DM"}),
    frozenset({"TG", "RG", "RM", "CG", "CM"}),
    frozenset({"TM"}),
    frozenset({})
)

target = (
    frozenset({}),
    frozenset({}),
    frozenset({}),
    frozenset(union(init))
)

Q = coll.deque()
seen = set()
came_from = {}
Q.append(init)

while Q:
    v = Q.popleft()
    if v == target:
        part2 = construct_path(v)
        break
    if v not in seen:
        seen.add(v)
        for n in adjacent(v):
            if n not in seen:
                Q.append(n)
                came_from[n] = v

# NB: This takes around 24 minutes to complete
print("Part 2:", part2)
