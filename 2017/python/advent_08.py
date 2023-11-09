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

lines = read_lines(8)

regs=defaultdict(int)
curmax=float("-inf")
for line in lines:
    instr,cond=line.split(" if ")
    if eval(re.sub(r"([a-z]+)",r"regs['\1']",cond)):
        target,op,amt=instr.split()
        if op=="inc":
            regs[target]+=int(amt)
        elif op=="dec":
            regs[target]-=int(amt)
        if regs[target]>curmax:
            curmax=regs[target]

part1 = max(regs.values())
print("Part 1:", part1)

part2 = curmax
print("Part 2:", part2)
