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

pos=A((0,0,0))
ds={
    "n":A((1,-1,0)),
    "ne":A((1,0,-1)),
    "nw":A((0,-1,1)),
    "s":A((-1,1,0)),
    "se":A((0,1,-1)),
    "sw":A((-1,0,1))
}
maxdist=0
for instr in lines[0].split(","):
    pos+=ds[instr]
    curdist=sum(abs(pos))//2
    if curdist>maxdist:
        maxdist=curdist

part1 = sum(abs(pos))//2
print("Part 1:", part1)

part2 = maxdist
print("Part 2:", part2)
