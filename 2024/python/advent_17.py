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

lines = read_lines(17)

a_part_1=0
program=[]
for line in lines:
    if line.startswith("Register A"):
        _,num,val=line.split()
        a_part_1=int(val)
    elif line.startswith("Program"):
        program=parse_ints(line)

# The provided program is an implementation of this alg
def run(val):
    A,B=val,0
    out=[]
    while A != 0:
        B=(A&7)^2
        B^=(A>>B)
        A>>=3
        out.append((B^7)&7)
    return out

part1 = ",".join(str(v) for v in run(a_part_1))

print("Part 1:", part1)

def neighbors(p):
    num,digits=p
    if digits==16:
        return
    prefix=program[:digits+1]
    for i in range(1024):
        n = i*8**digits + num
        attempt = run(n)
        if attempt[:digits+1] == prefix:
            yield n,digits+1

part2=min(p for (p,n) in bfs((0,0),false,neighbors) if n == 16)
print("Part 2:", part2)
