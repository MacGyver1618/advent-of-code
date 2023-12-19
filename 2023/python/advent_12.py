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

@func.cache
def recur(conf, groups, i, gi, gc):
    if i==len(conf):
        if gi==len(groups) and gc==0: # finished all groups
            return 1
        elif gi==len(groups)-1 and gc==groups[-1]: # at end of pattern and group complete
            return 1
        else: # unplaced tiles remaining
            return 0
    res=0
    for c in "#.":
        if conf[i] in [c,"?"]:
            if c=="#": # extend current group
                res+=recur(conf, groups, i + 1, gi, gc + 1)
            elif gc==0: # continue without starting new group
                res+=recur(conf, groups, i + 1, gi, gc)
            elif gi<len(groups) and groups[gi]==gc: # continue and end current group
                res+=recur(conf, groups, i + 1, gi + 1, 0)
    return res

def solve(repeats):
    tot=0
    progress=ProgressBar(1000)
    for line in lines:
        progress.update()
        conf,nos=line.split()
        groups=[*map(int,nos.split(","))]
        res=recur("?".join([conf] * repeats), tuple(groups * repeats), 0, 0, 0)
        tot+=res
    progress.clear()
    return tot

part1 = solve(1)
print("Part 1:", part1)

part2 = solve(5)
print("Part 2:", part2)

# for ln,line in enumerate(lines):
#     progress.update()
#     conf,nos=line.split()
#     groups=[*map(int,nos.split(","))]
#     qs=[i for i,c in enumerate(conf) if c=="?"]
#     l=len(qs)
#     r1=conf.replace(".","\\.").replace("?",".")
#     r2="\\.*"+"\\.+".join("#"*g for g in groups)+"\\.*"
#     for i in range(2**l):
#         s=[c for c in conf]
#         for j in range(l):
#             s[qs[j]]="#" if i & (1<<j) else "."
#         s="".join(s)
#         if re.fullmatch(r1,s) and re.fullmatch(r2,s):
#             tot+=1
# progress.clear()
