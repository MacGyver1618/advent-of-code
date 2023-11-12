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

lines = read_lines(6)
points=[tuple(map(int,line.split(", "))) for line in lines]
cmin=min(c for c,r in points)
cmax=max(c for c,r in points)
rmin=min(r for c,r in points)
rmax=max(r for c,r in points)
closest=defaultdict(int)
infinites=set()
for r in range(rmin,rmax+1):
    for c in range(cmin,cmax+1):
        ds=sorted([(p,manhattan_distance((c,r),p)) for p in points], key=second)
        if ds[0][1]!=ds[1][1]:
            p=ds[0][0]
            closest[p]+=1
            if r in [rmin,rmax] or c in [cmin,cmax]:
                infinites.add(p)

part1 = max(item[1] for item in closest.items() if item[0] not in infinites)
print("Part 1:", part1)

eligibles=0
for r in range(rmin,rmax+1):
    for c in range(cmin,cmax+1):
        total_dist=sum(manhattan_distance(p,(c,r)) for p in points)
        if total_dist<10_000:
            eligibles+=1
part2=eligibles
print("Part 2:", part2)
