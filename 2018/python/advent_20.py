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

lines = read_lines(20)

edges=set()
positions={0}
stack=[]
starts={0}
ends=set()
directions={"N":-1j,"S":1j,"W":-1,"E":1}

for c in lines[0][1:-1]:
    if c == "(":
        stack.append((starts,ends))
        starts=positions
        ends=set()
    if c == "|":
        ends.update(positions)
        positions=starts
    if c == ")":
        positions.update(ends)
        starts,ends=stack.pop()
    if c in "NEWS":
        d=directions[c]
        edges.update({(p,p+d) for p in positions})
        edges.update({(p+d,p) for p in positions})
        positions={p+d for p in positions}

def print_grid():
    nodes=set()
    nodes.update(a for a,b in edges)
    nodes.update(b for a,b in edges)
    Cmax=int(max(p.real for p in nodes))
    Rmax=int(max(p.imag for p in nodes))
    Cmin=int(min(p.real for p in nodes))
    Rmin=int(min(p.imag for p in nodes))

    print("#"*int(2*(Cmax-Cmin)+3))

    for r in range(Rmin,Rmax+1):
        if r>Rmin:
            s="#"
            for c in range(Cmin,Cmax+1):
                p=c+1j*r
                s+=" " if (p,p-1j) in edges else "#"
                s+="#"
            print(s)
        s="# "
        for c in range(Cmin+1,Cmax+1):
            p=c+1j*r
            s+=" " if (p,p-1) in edges else "#"
            s+=" "

        print(s+"#")

    print("#"*int(2*(Cmax-Cmin)+3))

lengths,_=dijkstra(0,lambda _:False,lambda p:[p+d for d in directions.values() if (p,p+d) in edges],lambda _,_2:1)

part1 = max(lengths.values())
print("Part 1:", part1)

part2 = sum(1 for l in lengths.values() if l >= 1000)
print("Part 2:", part2)
