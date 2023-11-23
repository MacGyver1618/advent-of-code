from fractions import Fraction

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
import math

lines = read_lines(10)

R=len(lines)
C=len(lines[0])

asteroids=set()
for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char == "#":
            asteroids.add((r,c))

visibility = defaultdict(set)

for r,c in asteroids:
    for r2,c2 in asteroids:
        if (r,c)==(r2,c2):
            continue
        ydiff = r2-r
        xdiff = c2-c
        if xdiff==0:
            visibility[(r,c)].add((sgn(ydiff),0))
        elif ydiff==0:
            visibility[(r,c)].add((0,sgn(xdiff)))
        else:
            gcd = sym.gcd(ydiff,xdiff)
            ydiff //= gcd
            xdiff //= gcd
            visibility[(r,c)].add((ydiff,xdiff))

part1 = max(len(v) for v in visibility.values())
print("Part 1:", part1)

start,angles = sorted(visibility.items(),key=lambda i: len(i[1]))[-1]
by_slope = sorted(angles,key=lambda a: math.atan2(*a))
pops = 0
i=by_slope.index((-1,0))
while pops < 200:
    r,c=start
    dr,dc = by_slope[i]
    while 0<=r<R and 0<=c<C:
        r+=dr
        c+=dc
        if (r,c) in asteroids:
            pops += 1
            asteroids.remove((r,c))
            part2=100*c+r
            break
    i = (i+1)%len(by_slope)

print("Part 2:", part2)
