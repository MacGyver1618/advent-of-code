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

map, instructions = full_input(22).split("\n\n")

grid = defaultdict(lambda: ".")


for r, line in enumerate(map.split("\n")):
    for c, char in enumerate(line):
        if char in "#.":
            grid[r,c] = char

U = A([-1, 0])
R = A([0, 1])
D = A([1, 0])
L = A([0, -1])
# coordinate axes swapped
RIGHT = L_turn
LEFT = R_turn
Rmin = min(r for r,c in grid)
Cmin = min(c for r,c in grid if r == Rmin)
position = A([Rmin,Cmin])
orientation = R

path = [tuple(position)]
def move(amount):
    for _ in range(amount):
        global  position
        npos = position+orientation
        if tuple(npos) not in grid:
            if (orientation == U).all():
                nr = max(r for r,c in grid if c == position[1])
                npos = A([nr, position[1]])
            elif (orientation == R).all():
                nc = min(c for r,c in grid if r == position[0])
                npos = A([position[0],nc])
            elif (orientation == D).all():
                nr = min(r for r,c in grid if c == position[1])
                npos = A([nr, position[1]])
            elif (orientation == L).all():
                nc = max(c for r,c in grid if r == position[0])
                npos = A([position[0], nc])
        if tuple(npos) in grid and grid[tuple(npos)] == ".":
            position = npos
            path.append(tuple(npos))
            continue
        if grid[tuple(npos)] == "#":
            continue

rr = min(r for r,c in grid)
cc = min(c for r,c in grid)
RR = max(r for r,c in grid)
CC = max(c for r,c in grid)
ors = [tuple(R), tuple(D), tuple(L), tuple(U)]

def print_grid():
    for r in range(rr,RR+1):
        s = ""
        for c in range(cc,CC+1):
            if (r,c) in path:
                s += "o"
            elif (r,c) in grid:
                s += grid[(r,c)]
            else:
                s += " "
        print(s)

def print_square():
    pr,pc = position
    sr = (pr//50)*50
    sc = (pc//50)*50
    print("+"+"-"*50+"+")
    for r in range(sr,sr+50):
        s = "|"
        for c in range(sc,sc+50):
            if (r,c) in path:
                s += path[(r,c)]
            elif grid[(r,c)] == "#":
                s += "#"
            else:
                s += " "
        s += "|"
        print(s)
    print("+"+"-"*50+"+")

squares = {
    ("A","U"):("F","R"),
    ("A","R"):("B","R"),
    ("A","D"):("C","D"),
    ("A","L"):("D","R"),

    ("B","U"):("F","U"),
    ("B","R"):("E","L"),
    ("B","D"):("C","L"),
    ("B","L"):("A","L"),

    ("C","U"):("A","U"),
    ("C","R"):("B","U"),
    ("C","D"):("E","D"),
    ("C","L"):("D","D"),

    ("D","U"):("C","R"),
    ("D","R"):("E","R"),
    ("D","D"):("F","D"),
    ("D","L"):("A","R"),

    ("E","U"):("C","U"),
    ("E","R"):("B","L"),
    ("E","D"):("F","L"),
    ("E","L"):("D","L"),

    ("F","U"):("D","U"),
    ("F","R"):("E","U"),
    ("F","D"):("B","D"),
    ("F","L"):("A","D"),
}

for instruction in re.split(r"((?<=[RL])|(?=[RL]))", instructions):
    if not instruction:
        continue
    # print_grid()
    # print(f"facing {['right', 'down', 'left', 'right'][ors.index(tuple(orientation))]}")
    # input()
    if instruction == "R":
        orientation = RIGHT@orientation
    elif instruction == "L":
        orientation = LEFT@orientation
    else:
        move(int(instruction))

final_row = position[0]
final_col = position[1]
ors = [tuple(R), tuple(D), tuple(L), tuple(U)]
or_score = ors.index(tuple(orientation))

part1 = 1000*(final_row+1) + 4*(final_col+1) + or_score
print("Part 1:", part1)

position = A([Rmin,Cmin])
path = dict()
path[tuple(position)] = ">"
orientation = R

def square(pos):
    r,c = pos
    if 50 <= c < 100 and 0 <= r < 50:
        return "A"
    if 100 <= c < 150:
        return "B"
    if 50 <= c < 100 and 50 <= r < 100:
        return "C"
    if c < 50 and r < 150:
        return "D"
    if 50 <= c < 100:
        return "E"
    return "F"

def move2(amount):
    for _ in range(amount):
        global  position, orientation
        pr,pc = position
        rc = pc % 50
        rr = pr % 50
        npos = position+orientation
        nr,nc = npos
        nor = orientation
        if tuple(npos) not in grid:
            if (orientation == U).all():
                if 0 <= pc < 50: # D
                    nc = 50
                    nr = 50 + rc
                    nor = R
                elif 50 <= pc < 100: # A
                    nr = 150 + rc
                    nc = 0
                    nor = R
                elif 100 <= pc < 150: # B
                    nr = 199
                    nc = rc
                    nor = U
            elif (orientation == R).all():
                if 0 <= pr < 50: # B
                    nc = 99
                    nr = 149-rr
                    nor = L
                elif 50 <= pr < 100: # C
                    nr = 49
                    nc = 100 + rr
                    nor = U
                elif 100 <= pr < 150: # E
                    nc = 149
                    nr = 49 - rr
                    nor = L
                elif 150 <= pr < 200: # F
                    nr = 149
                    nc = 50 + rr
                    nor = U
            elif (orientation == D).all():
                if 0 <= pc < 50: # F
                    nr = 0
                    nc = 100 + rc
                    nor = D
                elif 50 <= pc < 100: # E
                    nc = 49
                    nr = 150 + rc
                    nor = L
                elif 100 <= pc < 150: # B
                    nc = 99
                    nr = 50 + rc
                    nor = L
            elif (orientation == L).all():
                if 0 <= pr < 50: # A
                    nc = 0
                    nr = 149-rr
                    nor = R
                elif 50 <= pr < 100: # C
                    nr = 100
                    nc = rr
                    nor = D
                elif 100 <= pr < 150: # D
                    nc = 50
                    nr = 49-rr
                    nor = R
                elif 150 <= pr < 200: # F
                    nr = 0
                    nc = 50 + rr
                    nor = D
            npos = A([nr,nc])
        if grid[tuple(npos)] == "#":
            break
        if tuple(npos) in grid and grid[tuple(npos)] == ".":
            position = npos
            orientation = nor
            path[tuple(npos)] = [">","v","<","^"][ors.index(tuple(orientation))]
i = 0
for instruction in re.split(r"((?<=[RL])|(?=[RL]))", instructions)[::2]:
    i += 1
    if instruction not in "RL":
        r,c = position
        r %= 50
        c %= 50
    if instruction == "R":
        orientation = RIGHT@orientation
    elif instruction == "L":
        orientation = LEFT@orientation
    else:
        move2(int(instruction))

final_row = position[0]
final_col = position[1]
ors = [tuple(R), tuple(D), tuple(L), tuple(U)]
or_score = ors.index(tuple(orientation))

part2 = 1000*(final_row+1) + 4*(final_col+1) + or_score
print("Part 2:", part2)
