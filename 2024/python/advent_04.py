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

lines = read_lines(4)
R = len(lines)
C = len(lines[0])

tot=0
for r0 in range(R):
    for c0 in range(C):
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                w = ""
                for i in range(4):
                    r=r0+i*dr
                    c=c0+i*dc
                    w += lines[r][c] if 0<=r<R and 0<=c<C else ""
                if w=="XMAS":
                    tot+=1
part1 = tot
print("Part 1:", part1)

xs = 0

mass = [["M.S",".A.","M.S"],["M.M",".A.","S.S"],["S.M",".A.","S.M"],["S.S",".A.","M.M"]]
def has_mas(subgrid):
    for mas in mass:
        matches=True
        for r,line in enumerate(mas):
            for c,sym in enumerate(line):
                if sym==".":
                    continue
                matches &= sym == subgrid[r][c]
        if matches:
            return True
    return False

for r in range(0, R-2):
    for c in range(0,C-2):
        subgrid=[line[c:c+3] for line in lines[r:r+3]]
        if has_mas(subgrid):
            xs+=1

part2 = xs
print("Part 2:", part2)
