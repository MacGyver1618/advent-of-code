import time

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

inpt = read_lines(23)

grid = defaultdict(lambda: " ")

R = len(inpt)
C = len(inpt[0])

orig = defaultdict(lambda: " ")

for r, line in enumerate(inpt):
    for c, char in enumerate(line):
        if char == "#":
            grid[(r,c)] = "#"
        if char in "ABCD":
            orig[(r,c)] = char

target = {
    (2,3): "A",
    (3,3): "A",
    (2,5): "B",
    (3,5): "B",
    (2,7): "C",
    (3,7): "C",
    (2,9): "D",
    (3,9): "D",
}

target_set = frozenset(target.items())
target_dict = defaultdict(lambda: " ")
for k,v in target.items():
    target_dict[k] = v

unit_costs = {
    "A":1,
    "B":10,
    "C":100,
    "D":1000,
}

def in_hallway(pos):
    return pos[0] == 1

def in_room(pos):
    return pos[0] > 1

def legal_moves(pos):
    if in_room(pos):
        for c in [1,2,4,6,8,10,11]:
            yield 1,c
    else:
        for r in [2,3]:
            for c in [3,5,7,9]:
                yield r,c

def cost_of_move(start, end, amph):
    return manhattan_distance(start, end)*unit_costs[amph]

def dist_fn(poss1, poss2):
    poss1 = dict(poss1)
    poss2 = dict(poss2)
    start = [p for p in poss1 if p not in poss2][0]
    end = [p for p in poss2 if p not in poss1][0]
    amph = poss1[start]
    return cost_of_move(start, end, amph)

def heur_fn(poss):
    As = sorted([p for p,a in poss if a == "A"])
    Bs = sorted([p for p,a in poss if a == "B"])
    Cs = sorted([p for p,a in poss if a == "C"])
    Ds = sorted([p for p,a in poss if a == "D"])
    vec = As + Bs + Cs + Ds
    return sum(map(lambda v: cost_of_move(*v), zip(vec, target.keys(), target.values())))

def path_between(p1,p2):
    r1,c1 = p1
    r2,c2 = p2
    if in_room(p1):
        vert = [(r,c1) for r in range(min(r1,r2),max(r1,r2)+1)][1:-1]
        hor = [(r2,c) for c in range(min(c1,c2), max(c1,c2)+1)]
        return vert + hor
    else:
        hor = [(r1,c) for c in range(min(c1,c2), max(c1,c2)+1)][1:-1]
        vert = [(r,c2) for r in range(min(r1,r2),max(r1,r2)+1)]
        return hor + vert

def is_blocked(p1,p2,poss):
    occupied = set(map(first,poss))
    path = path_between(p1,p2)
    return len([x for x in path if x in occupied]) > 0

def neighbor_fn(poss):
    for p1, amph in sorted(poss):
        for p2 in legal_moves(p1):
            temp = defaultdict(lambda: " ", poss)
            if is_blocked(p1,p2,poss):
                continue
            if in_room(p2):
                if target_dict[p2] != amph: # must move from hallway only into target room
                    continue
                room_occupants = {temp[(2,p2[1])], temp[(3,p2[1])]}
                if room_occupants.difference({" ", target_dict[p2]}): # room must be empty or contain only target dudes
                    continue
                if len(room_occupants.difference({" "})) == 0 and p2[0] != 3: # must move into bottom most slot if room is empty
                    continue
            temp.pop(p1)
            temp[p2] = amph
            yield frozenset([(k,v) for k,v in temp.items() if v != " "])

# ts = time.time()
# min_path = a_star(frozenset(orig.items()), lambda p: p == target_set, neighbor_fn, dist_fn, heur_fn)
# t = time.time() - ts
#
# prev = min_path[0]
# cost = 0
# for i in range(1,len(min_path)):
#     p = min_path[i]
#     cost += dist_fn(p, prev)
#     prev = p
# print("Part 1:", cost, "(", t, "s)")

grid = defaultdict(lambda: " ")
orig = defaultdict(lambda: " ")
inpt2 = [
    inpt[0],
    inpt[1],
    inpt[2],
    "  #D#C#B#A#",
    "  #D#B#A#C#",
    inpt[3],
    inpt[4]
]

for r, line in enumerate(inpt2):
    for c, char in enumerate(line):
        if char == "#":
            grid[(r,c)] = "#"
        if char in "ABCD":
            orig[(r,c)] = char
R += 2
target = {
    (2,3): "A",
    (3,3): "A",
    (4,3): "A",
    (5,3): "A",
    (2,5): "B",
    (3,5): "B",
    (4,5): "B",
    (5,5): "B",
    (2,7): "C",
    (3,7): "C",
    (4,7): "C",
    (5,7): "C",
    (2,9): "D",
    (3,9): "D",
    (4,9): "D",
    (5,9): "D",
}
target_set = frozenset(target.items())
target_dict = defaultdict(lambda: " ", target)

def legal_moves2(pos):
    if in_room(pos):
        for c in [1,2,4,6,8,10,11]:
            yield 1,c
    else:
        for r in [2,3,4,5]:
            for c in [3,5,7,9]:
                yield r,c

def neighbor_fn2(poss):
    for p1, amph in sorted(poss):
        for p2 in legal_moves2(p1):
            temp = defaultdict(lambda: " ", poss)
            if is_blocked(p1,p2,poss):
                continue
            if in_room(p2):
                if target_dict[p2] != amph: # must move from hallway only into target room
                    continue
                r,c = p2
                room_occupants = [temp[(2,c)], temp[(3,c)], temp[(4,c)], temp[(5,c)]]
                if set(room_occupants).difference({" ", target_dict[p2]}): # room must be empty or contain only target dudes
                    continue
                if target_dict[p2] != amph:
                    continue
                if room_occupants[3] == " " and r < 5:
                    continue
                if room_occupants[2] == " " and r < 4:
                    continue
                if room_occupants[1] == " " and r < 3:
                    continue
            temp.pop(p1)
            temp[p2] = amph
            yield frozenset([(k,v) for k,v in temp.items() if v != " "])

ts = time.time()
min_path = a_star(frozenset(orig.items()), lambda p: p == target_set, neighbor_fn2, dist_fn, heur_fn)
t = time.time() - ts

prev = min_path[0]
cost = 0
for i in range(1,len(min_path)):
    p = min_path[i]
    cost += dist_fn(p, prev)
    prev = p
print("Part 2:", cost, "(", t, "s)")
