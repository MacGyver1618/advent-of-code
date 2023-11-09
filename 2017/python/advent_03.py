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

N = int(read_lines(3)[0])
grid=dict()
n_grid=defaultdict(int)
dirs=[R,D,L,U]
step=1
cur=1
pos=O
di=0
sum_found=False
while cur<=N:
    for _ in range(step):
        grid[cur]=pos
        nsum=sum(n_grid[tuple(n)] for n in adjacent_diag(pos)) if cur > 1 else 1
        if nsum > N and not sum_found:
            part2=nsum
            sum_found=True
        n_grid[tuple(pos)]=nsum
        pos=pos+dirs[di]
        cur+=1
    di+=1
    if di==2:
        step+=1
    if di==4:
        di=0
        step+=1

print("Part 1:", manhattan_distance(O,grid[N]))

print("Part 2:", part2)
