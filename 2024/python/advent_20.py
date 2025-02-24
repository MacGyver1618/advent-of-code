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

lines = read_lines(20)
grid=Grid(lines)
R = len(lines)
C = len(lines[0])

for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char=="E":
            end=(r,c)
            grid.place(end, ".")
        elif char=="S":
            start=(r,c)
            grid.place(start, ".")

def neighbors(p):
    return [tuple(n) for n in grid.neighbors(p) if grid.char_at(n) != "#"]

path = bfs(start, eq(end), neighbors)
grid.print(custom_points={**{p:"O" for p in path},start:"S", end: "E"}, highlights={"S":95,"E":95,"O":93,"#":90})

part1=0
part2=0
for p1,p2 in it.combinations(enumerate(path),2):
    d = manhattan_distance(p1[1],p2[1])
    if d <= 20:
        cheat=abs(p1[0]-p2[0])-d
        if cheat >= 100:
            part2+=1
            if d==2:
                part1+=1
print("Part 1:", part1)
print("Part 2:", part2)
