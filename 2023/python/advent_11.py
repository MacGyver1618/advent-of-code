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

lines = read_lines(11)

rows=defaultdict(int)
cols=defaultdict(int)
galaxies=set()
for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char=="#":
            rows[r]+=1
            cols[c]+=1
            galaxies.add((r,c))

def dist_fn(a,b,w):
    c1,c2=sorted((a[1],b[1]))
    r1,r2=sorted((a[0],b[0]))
    return manhattan_distance(a,b)+(w-1)*(sum(1 for r in range(r1,r2) if not rows[r])+sum(1 for c in range(c1,c2) if not cols[c]))

part1 = sum(dist_fn(a,b,2) for a in galaxies for b in galaxies)//2
print("Part 1:", part1)
part2=sum(dist_fn(a,b,1_000_000) for a in galaxies for b in galaxies)//2
print("Part 2:", part2)
