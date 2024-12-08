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

lines = read_lines(7)

def is_valid(res, ops, part2=False):
    cur=ops[0]
    if len(ops)==1:
        return cur==res
    if part2 and is_valid(res, [int(f"{cur}{ops[1]}")]+ops[2:], part2):
        return True
    if is_valid(res, [cur*ops[1]]+ops[2:], part2):
        return True
    if is_valid(res, [cur+ops[1]]+ops[2:], part2):
        return True
    return False

part1=0
part2=0
pb=ProgressBar(len(lines))
for line in lines:
    pb.update()
    res,ops=line.split(": ")
    res=int(res)
    ops=[*map(int,ops.split())]
    if is_valid(res, ops):
        part1+=res
    if is_valid(res,ops,True):
        part2+=res

pb.clear()
print("Part 1:", part1)
print("Part 2:", part2)
