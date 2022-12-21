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

lines = read_lines(14)

cave = {}
spigot = (500,0)
for line in lines:
    start, *rest = line.split(" -> ")
    x0,y0 = to_nums(start.split(","))
    cave[(x0,y0)] = "#"
    for wp in rest:
        x1,y1 = to_nums(wp.split(","))
        cave[(x1,y1)] = "#"
        dx,dy = sgn(x1-x0),sgn(y1-y0)
        x,y = x0,y0
        while x != x1 or y != y1:
            x += dx
            y += dy
            cave[(x,y)] = "#"
        x0,y0 = x1,y1
xmin = min([first(p) for p in cave])
xmax = max([first(p) for p in cave])
ymin = min([second(p) for p in cave])
ymax = max([second(p) for p in cave])

floor = ymax+2
for x in range(-1000,1000):
    cave[(x,floor)] = "#"

def print_cave(grain_pos):
    px,py = grain_pos
    ydiff = 20
    if py in range(0,ydiff+1):
        wmin,wmax = 0,2*ydiff+1
    elif py in range(floor-ydiff, floor+1):
        wmin,wmax = floor-2*ydiff-1,floor+1
    else:
        wmin,wmax = py-ydiff,py+ydiff+1
    ss = []
    for y in range(wmin, wmax+1):
        s = []
        for x in range(xmin, xmax+1):
            if (x,y) == grain_pos:
                s.append("o")
            elif (x,y) == spigot:
                s.append("+")
            else:
                s.append(cave[(x,y)] if (x,y) in cave else " ")
        ss.append("".join(s))
    return ss

part1 = 0
sand = 0
full = False
frames = []
pos = spigot
while not full:
    sand += 1
    frames.append(print_cave(pos))
    print(sand)
    pos = spigot
    found = False
    while not found:
        x,y = pos
        if y >= ymax and part1 == 0:
            part1 = sand-1
        npos = (x,y+1)
        if npos not in cave:
            pos = npos
            continue
        npos = (x-1,y+1)
        if npos not in cave:
            pos = npos
            continue
        npos = (x+1,y+1)
        if npos not in cave:
            pos = npos
            continue
        if y == 0:
            full = True
        cave[pos] = "o"
        found = True

print("Part 1:", part1)
print("Part 2:", sand)

for frame in frames:
    print("\n".join(frame))
    time.sleep(0.1)