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

lines, instrs=full_input(15).strip().split("\n\n")
lines = lines.split("\n")
grid=Grid(lines)
instrs=instrs.split("\n")

robot=None

for (r,c),val in grid.items():
    if val=="@":
        robot=A((r,c))
        grid.raw_grid[r][c]="."

Ds={"^":A((-1,0)),"v":A((1,0)),"<":A((0,-1)),">":A((0,1))}


for line in instrs:
    for char in line:
        step=Ds[char]
        nxt=grid.char_at(robot+step)
        if nxt==".":
            robot+=step
        elif nxt=="O":
            pos=robot+step
            while grid.char_at(pos)=="O":
                pos+=step
            if grid.char_at(pos) == ".":
                robot+=step
                grid.place(pos, "O")
                grid.place(robot, ".")

part1 = sum(100*r+c for (r,c) in grid.points() if grid.char_at((r,c))=="O")
print("Part 1:", part1)

lines2=[]
for r,line in enumerate(lines):
    line2=""
    for c,char in enumerate(line):
        if char == "O":
            line2+="[]"
        elif char=="@":
            robot=A((r,2*c))
            line2+=".."
        else:
            line2+=char*2
    lines2+=[line2]

grid=Grid(lines2)
grid.print(custom_points={tuple(robot):"\033[93m@\033[39m"},header="\033[2J")
#input()


for i,char in enumerate(''.join(instrs)):
    step=Ds[char]
    pos = robot + step
    nxt=grid.char_at(pos)
    if nxt==".":
        robot+=step
    elif nxt in "[]":
        if char in "<>":
            while grid.char_at(pos) in "[]":
                pos+=step
            if grid.char_at(pos) == ".":
                while any(pos != robot):
                    cur=grid.char_at(pos)
                    grid.place(pos, grid.char_at(pos-step))
                    grid.place(pos-step, cur)
                    pos-=step
                robot+=step
        else: # moving vertically, the hard part
            stack=[]
            if nxt=="[":
                frontier=[pos,pos+(0,1)]
            else:
                frontier=[pos+(0,-1),pos]
            stack.append(frontier)
            while True:
                fringe=[grid.char_at(f+step) for f in frontier]
                if "#" in fringe:
                    break # can't move stack
                if "[" not in fringe and "]" not in fringe:
                    while stack:
                        cur=stack.pop()
                        for c in cur:
                            n=grid.char_at(c+step)
                            grid.place(c+step, grid.char_at(c))
                            grid.place(c, n)
                    robot+=step
                    break
                frontier=[f+step for f in frontier if grid.char_at(f+step) in "[]"]
                for f in frontier:
                    if grid.char_at(f)=="]" and tuple(n:=f+(0,-1)) not in [tuple(f) for f in frontier]:
                        frontier+=[n]
                    if grid.char_at(f)=="[" and tuple(n:=f+(0,1)) not in [tuple(f) for f in frontier]:
                        frontier+=[n]
                stack.append(frontier)

    grid.print(header=f"\033[2J{i}/{sum(len(l) for l in instrs)}",custom_points={tuple(robot):"@"},highlights={".":90,"[":35,"]":35,"#":34,"@":93})
    time.sleep(0.05)

part2 = sum(100*r+c for (r,c) in grid.points() if grid.char_at((r,c))=="[")
print("Part 2:", part2)
