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

instructions = read_lines(17)[0]

shapes = [
    ["####"],
    [" # ",
     "###",
     " # "],
    ["###",
     "  #",
     "  #"],
    ["#",
     "#",
     "#",
     "#"],
    ["##",
     "##"],
]

column = defaultdict(lambda: " ")
cursor = 0
floor = 0

def print_column(rock, rock_pos):
    rr, rc = rock_pos
    rh = len(rock)
    rw = len(rock[0])
    for r in range(max(floor, rr+rh)-1,-1,-1):
        s = "|"
        for c in range(7):
            if rr <= r < rr+rh and rc <= c < rc+rw and rock[r-rr][c-rc] == "#":
                s += "@"
            else:
                s += column[(r,c)]
        s += "|"
        print(s)
    print("+-------+")


def collides(rock, rock_pos, delta):
    rh = len(rock)
    rw = len(rock[0])
    rr,rc = rock_pos
    dr,dc = delta
    if rr == 0 and dr == -1: # fall through bottom
        return True
    if rc == 0 and dc == -1: # push through left wall
        return True
    if rc+rw == 7 and dc == 1: # push through right wall
        return True
    for r in range(rh):
        for c in range(rw):
            if rock[r][c] == "#" and column[(rr+r+dr,rc+c+dc)] == "#":
                return True
    return False

part1 = -1
part2 = -1
rocks = 0
hist = []
while part1 == -1 or part2 == -1:
    if rocks == 2022:
        part1 = floor
    rock = shapes[rocks%5]
    rh = len(rock)
    rw = len(rock[0])
    rr = floor+3
    rc = 2
    while True:
        gust = instructions[cursor]
        cursor = (cursor + 1) % len(instructions)
        if cursor == 0 and floor > 0:
            if hist:
                print(rocks-hist[-1][0], floor-hist[-1][1])
            hist.append((rocks, floor))
            print(rocks,floor)
            input()
        if hist and rocks-hist[-1][0] == 1585 and hist:
            print(floor-hist[-1][1])
        if gust == ">" and not collides(rock, (rr,rc), (0,1)):
            rc += 1
        elif gust == "<" and not collides(rock, (rr,rc), (0,-1)):
            rc -= 1
        if not collides(rock, (rr,rc), (-1,0)):
            rr -= 1
        else:
            for y in range(rr, rr+rh):
                for x in range(rc, rc+rw):
                    if rock[y-rr][x-rc] == "#":
                        column[y,x] = rock[y-rr][x-rc]
            floor = max(y for (y,x),v in column.items() if v == "#")+1
            break
    rocks += 1

print("Part 1:", part1)
print("Part 2:", part2)