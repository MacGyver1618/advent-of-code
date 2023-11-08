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

lines = read_lines(23)

elves = set()

for r,line in enumerate(lines):
    for c, char in enumerate(line):
        if char == "#":
            elves.add((r,c))

def has_neighbors(elf):
    r,c = elf
    for dr in [-1,0,1]:
        for dc in [-1,0,1]:
            if (dr,dc) != (0,0) and (r+dr,c+dc) in elves:
                return True
    return False

def neighbors_north(elf):
    r,c = elf
    for dc in [-1,0,1]:
        if (r-1,c+dc) in elves:
            return True
    return False

def neighbors_south(elf):
    r,c = elf
    for dc in [-1,0,1]:
        if (r+1,c+dc) in elves:
            return True
    return False

def neighbors_west(elf):
    r,c = elf
    for dr in [-1,0,1]:
        if (r+dr,c-1) in elves:
            return True
    return False

def neighbors_east(elf):
    r,c = elf
    for dr in [-1,0,1]:
        if (r+dr,c+1) in elves:
            return True
    return False

def move_to(delta):
    dr,dc = delta
    def apply(elf):
        r,c = elf
        return r+dr,c+dc
    return apply

tries = deque()
tries.append((neighbors_north, move_to((-1, 0))))
tries.append((neighbors_south, move_to(( 1, 0))))
tries.append((neighbors_west,  move_to(( 0,-1))))
tries.append((neighbors_east,  move_to(( 0, 1))))

part1 = 0
part2 = 0
while True:
    part2 += 1
    if part2 == 11:
        rmin = min(r for r,c in elves)
        rmax = max(r for r,c in elves)
        cmin = min(c for r,c in elves)
        cmax = max(c for r,c in elves)
        for r in range(rmin, rmax+1):
            for c in range(cmin, cmax+1):
                if (r,c) not in elves:
                    part1 += 1
    proposals = defaultdict(list)
    next_elves = set()
    for elf in elves:
        r,c = elf
        if not has_neighbors(elf):
            next_elves.add(elf)
            continue
        if not tries[0][0](elf):
            proposals[tries[0][1](elf)].append(elf)
            continue
        if not tries[1][0](elf):
            proposals[tries[1][1](elf)].append(elf)
            continue
        if not tries[2][0](elf):
            proposals[tries[2][1](elf)].append(elf)
            continue
        if not tries[3][0](elf):
            proposals[tries[3][1](elf)].append(elf)
            continue
        next_elves.add(elf)
    moves = 0
    for proposal, candidates in proposals.items():
        if len(candidates) > 1:
            for candidate in candidates:
                next_elves.add(candidate)
        else:
            moves += 1
            next_elves.add(proposal)
    if moves == 0:
        break
    elves = next_elves
    tries.rotate(-1)

print("Part 1:", part1)
print("Part 2:", part2)
