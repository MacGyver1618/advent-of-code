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

lines = read_lines(22)
R = len(lines)
C = len(lines[0])

xmin,xmax,ymin,ymax,zmin,zmax=0,0,0,0,0,0
bricks=[]
for line in lines:
    sx,sy,sz,ex,ey,ez=map(int,re.findall(r"\d+",line))
    xmin=min(xmin,sx)
    xmax=max(xmax,ex)
    ymin=min(ymin,sy)
    ymax=max(ymax,ey)
    zmin=min(zmin,sz)
    zmax=max(zmax,ez)
    bricks.append(((sx,sy,sz),(ex,ey,ez)))

grid=[[[-1]*(xmax+1) for _ in range(ymax+1)] for _ in range(zmax+1)]

fallen=[]
Q=deque(enumerate(sorted(bricks,key=lambda b: b[0][2])))
while Q:
    i,brick=Q.popleft()
    (sx,sy,sz),(ex,ey,ez)=brick
    while sz>1 and all(grid[sz-1][y][x]==-1 for y in range(sy,ey+1) for x in range(sx,ex+1)):
        sz-=1
        ez-=1
    for x in range(sx,ex+1):
        for y in range(sy,ey+1):
            for z in range(sz,ez+1):
                grid[z][y][x]=i
    fallen.append(((sx,sy,sz),(ex,ey,ez)))

def bricks_above(brick):
    (sx,sy,sz),(ex,ey,ez)=brick
    above=set()
    for y in range(sy,ey+1):
        for x in range(sx,ex+1):
            above.add(grid[ez+1][y][x])
    above.difference_update({-1})
    return above

def bricks_below(brick):
    (sx,sy,sz),(ex,ey,ez)=brick
    below=set()
    for y in range(sy,ey+1):
        for x in range(sx,ex+1):
            below.add(grid[sz-1][y][x])
    below.difference_update({-1})
    return below

part1=0
outbound=defaultdict(set)
for i,brick in enumerate(fallen):
    (sx,sy,sz),(ex,ey,ez)=brick
    above=bricks_above(brick)
    outbound[i].update(above)
    if len(above)==0 or all(len(bricks_below(fallen[other]))>1 for other in above):
        part1+=1

print("Part 1:", part1)

part2=0
outbound[-1]= {i for i,b in enumerate(fallen) if b[0][2] == 1}
pb=ProgressBar(len(fallen))
for i,brick in enumerate(fallen):
    pb.update()
    visitable=bfs(-1,lambda _:False, lambda p: [n for n in outbound[p] if n!=i])
    part2+=len(fallen)-len(visitable)

pb.clear()
print("Part 2:", part2)
