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

lines = read_lines(9)

disk=[]

file=True
i=0
for c in lines[0]:
    if file:
        disk+=[i for _ in range(int(c))]
        i+=1
    else:
        disk+=[-1 for _ in range(int(c))]
    file=not file

lo=0
hi=len(disk)-1

while lo<hi:
    while lo<len(disk) and disk[lo]!=-1:
        lo+=1
    while hi >= 0 and disk[hi]==-1:
        hi-=1
    if lo>=hi:
        break
    t=disk[hi]
    disk[hi]=disk[lo]
    disk[lo]=t

part1 = sum(i*n for i,n in enumerate(disk) if n!=-1)
print("Part 1:", part1)

def parse_blocks(line):
    blocks = []
    file=True
    i=0
    for c in line:
        if file:
            blocks+=[[i for _ in range(int(c))]]
            i+=1
        else:
            blocks+=[[-1 for _ in range(int(c))]]
        file=not file
    return blocks

blocks=parse_blocks(lines[0])
i=len(blocks)-1
pb=ProgressBar(len(blocks))
while i>=0:
    pb.update()
    while i>=0 and len(blocks[i])>0 and blocks[i][0]==-1:
        i-=1
    if i < 0:
        break
    block=blocks[i]
    size=len(block)
    free=[(n,b) for n,b in enumerate(blocks[:i]) if len(b)>=size>0 and b[0]==-1]
    if not free:
        i-=1
        continue
    n,b=free[0]
    blocks=blocks[:n]+[block]+[[-1 for _ in range(len(b)-size)]]+blocks[n+1:i]+[[-1 for _ in range(size)]]+blocks[i+1:]

pb.clear()

disk=[n for block in blocks for n in block]
part2=sum(i*n for i,n in enumerate(disk) if n!=-1)
print("Part 2:", part2)
