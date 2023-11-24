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

lines = read_lines(12)
PX,PY,PZ,VX,VY,VZ=0,1,2,3,4,5
moons=[]
for line in lines:
    x,y,z=map(int,re.findall(r"-?\d+",line))
    moons += [[x,y,z,0,0,0]]

x0,y0,z0=[[p for moon in moons for p in [moon[i],moon[i+3]]] for i in range(3)]

t=0
for _ in range(1000):
    new_moons=[]
    for moon in moons:
        next_moon=moon.copy()
        for other in moons:
            if other==moon:
                continue
            for i in range(3):
                next_moon[i+3]+=sgn(other[i]-moon[i])
        for i in range(3):
            next_moon[i] += next_moon[i+3]
        new_moons.append(next_moon)
    moons=new_moons
    t+=1
    x1,y1,z1=[[p for moon in moons for p in [moon[i],moon[i+3]]] for i in range(3)]

part1=sum(sum(map(abs,moon[:3]))*sum(map(abs,moon[3:])) for moon in moons)
print("Part 1:", part1)

cycx,cycy,cycz=None,None,None

while not all([cycx,cycy,cycz]):
    new_moons=[]
    for moon in moons:
        next_moon=moon.copy()
        for other in moons:
            if other==moon:
                continue
            for i in range(3):
                next_moon[i+3]+=sgn(other[i]-moon[i])
        for i in range(3):
            next_moon[i] += next_moon[i+3]
        new_moons.append(next_moon)
    moons=new_moons
    t+=1
    x1,y1,z1=[[p for moon in moons for p in [moon[i],moon[i+3]]] for i in range(3)]
    if x1==x0 and not cycx:
        cycx=t
    if y1==y0 and not cycy:
        cycy=t
    if z1==z0 and not cycz:
        cycz=t
part2=sym.lcm(cycx,sym.lcm(cycy,cycz))
print("Part 2:", part2)
