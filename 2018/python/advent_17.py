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

lines = read_lines(17)

grid=defaultdict(lambda:' ')
grid[0,500]="+"
for line in lines:
    const,_range=line.split(", ")
    dim,val=const.split("=")
    val=int(val)
    _,vals=_range.split("=")
    start,end=map(int,vals.split(".."))
    for var in range(start,end+1):
        if dim=="x":
            grid[(var,val)]="#"
        else:
            grid[(val,var)]="#"
Rmin= min(r for (r,c),v in grid.items() if v=="#")
Rmax= max(r for r,c in grid.keys()) + 1
Cmin=min(c for r,c in grid.keys())-1
Cmax=max(c for r,c in grid.keys())+2

def print_grid(bounds=[0, Rmax, Cmin, Cmax]):
    ss=[]
    for r in range(bounds[0],bounds[1]):
        s=""
        for c in range(bounds[2],bounds[3]):
            s+=grid[(r,c)]
        ss+=[s]
    print("\n".join(ss))

def expand_horizontal(r,c):
    rc=c
    lc=c
    while True:
        below=grid[r+1,lc]
        if below in " |":
            left_edge="cliff"
            break
        to_left=grid[r,lc-1]
        if to_left=="#":
            left_edge="wall"
            break
        lc-=1
    while True:
        below=grid[r+1,rc]
        if below in " |":
            right_edge="cliff"
            break
        to_right=grid[r,rc+1]
        if to_right=="#":
            right_edge="wall"
            break
        rc+=1

    if [left_edge, right_edge]==["wall","wall"]:
        for c1 in range(lc, rc+1):
            grid[r,c1]="~"
        return expand_horizontal(r-1,c)

    for c1 in range(lc, rc+1):
        grid[r,c1]="|"
    new_drips=[]
    if left_edge=="cliff":
        new_drips+=[(r,lc)]
    if right_edge=="cliff":
        new_drips+=[(r,rc)]
    return new_drips


water_level=0
drips=deque([(0,500)])
prompt=""
skip=0
while drips:
    drip=drips.popleft()
    prompt=""
    # if skip == 0:
    #     print_grid([max(water_level-20,0),max(water_level+21,41),Cmin,Cmax])
    #     _input=input(prompt)
    #     while _input:
    #         command=_input[0]
    #         if command in "du":
    #             amt=1 if len(_input)<1 else int(_input[1:].strip())
    #             water_level+=amt if command=="d" else -amt
    #             prompt=f"Water level is now {water_level}"
    #             print_grid([max(water_level-20,0),max(water_level+21,41),Cmin,Cmax])
    #             _input=input(prompt)
    #         elif command == "s":
    #             amt=1 if len(_input)<1 else int(_input[1:].strip())
    #             skip+=amt
    #             prompt=f"Skipped {skip} turns"
    #             _input=""
    # else:
    #     skip = max(skip-1,0)
    r,c=drip
    below=grid[r+1,c]
    if below==" ":
        grid[r+1,c]="|"
        if r<Rmax-2:
            drips.append((r+1,c))
    if below in "#~":
        for new_drip in expand_horizontal(r,c):
            if new_drip[0]<=Rmax:
                drips.append(new_drip)

# print_grid([max(water_level-20,0),max(water_level+21,41),Cmin,Cmax])
# _input=input(prompt)
# while _input:
#     command=_input[0]
#     if command in "du":
#         amt=1 if len(_input)<1 else int(_input[1:].strip())
#         water_level+=amt if command=="d" else -amt
#         prompt=f"Water level is now {water_level}"
#         print_grid([max(water_level-20,0),max(water_level+21,41),Cmin,Cmax])
#         _input=input(prompt)
part1 = sum(1 for k,v in grid.items() if v in "~|" and Rmin<=k[0]<Rmax)
print("Part 1:", part1)

part2 = sum(1 for v in grid.values() if v in "~")
print("Part 2:", part2)
