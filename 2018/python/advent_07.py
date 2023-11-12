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
nodes=set()
edges=set()
for line in lines:
    a=line.split()[1]
    b=line.split()[-3]
    nodes.add(a)
    nodes.add(b)
    edges.add((a,b))

L=[]
remaining_edges=edges.copy()
while len(L)<len(nodes):
    available=sorted([n for n in nodes if n not in [b for a,b in remaining_edges] and n not in L],reverse=True)
    _next=available.pop()
    L+=[_next]
    for e in [(a,b) for a,b in remaining_edges if a==_next]:
        remaining_edges.remove(e)


part1 = "".join(L)
print("Part 1:", part1)

L=[]
remaining_edges=edges.copy()
workers=[[".",0] for _ in range(5)]
secs=0
while len(L)<len(nodes):
    for worker in workers:
        c,r=worker
        if c!='.':
            worker[1]-=1
            if worker[1]==0:
                L+=[worker[0]]
                for e in [(a,b) for a,b in remaining_edges if a==worker[0]]:
                    remaining_edges.remove(e)
                worker[0]='.'
    Q=[c for c,r in workers if c!='.']
    available=sorted([n for n in nodes if n not in [b for a,b in remaining_edges] and n not in L and n not in Q],reverse=True)
    for worker in workers:
        c,r=worker
        if c=='.' and available:
            _next=available.pop()
            worker[0]=_next
            worker[1]=ord(_next)-4
    secs+=1

part2 = secs-1
print("Part 2:", part2)
