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

lines = read_lines(10)

points=[]
for line in lines:
    x,y,vx,vy=map(int,re.findall(r"-?\d+",line))
    points.append((x,y,vx,vy))

def bounding_box(ps):
    xs = [x for x,*_ in ps]
    ys = [y for _,y,*_ in ps]
    return (max(xs)-min(xs))*(max(ys)-min(ys))
i=0
while True:
    bb=bounding_box(points)
    next_points=[(x+vx,y+vy,vx,vy) for x,y,vx,vy in points]
    next_bb=bounding_box(next_points)
    if next_bb > bb:
        break
    i+=1
    points=next_points

print("Part 1:")

xs = [x for x,*_ in points]
ys = [y for _,y,*_ in points]
poss =[(y,x) for x,y,*_ in points]
for r in range(min(ys),max(ys)+1):
    s=""
    for c in range(min(xs),max(xs)+1):
        s+="*" if (r,c) in poss else " "
    print(s)

part2 = i
print("Part 2:", part2)
