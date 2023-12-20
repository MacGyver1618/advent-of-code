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
edges=defaultdict(list)
conjunctions={}
flipflops={}
nodes=set()
wires=defaultdict(dict)

for line in lines:
    module, outs=line.split(" -> ")
    outs=outs.split(", ")
    _type=module[0]
    node=module.lstrip("%&")
    nodes.add(node)
    nodes.update(outs)
    edges[node]=outs
    if _type=="%":
        flipflops[node]=False
    elif _type=="&":
        conjunctions[node]={}
    for out in outs:
        wires[out][node]=False

lows,highs=0,0
def neighbors(state):
    global lows,highs
    node,signal,source=state
    if signal:
        highs+=1
    else:
        lows+=1
    if node in flipflops:
        if signal:
            return []
        else:
            flipflops[node]=not flipflops[node]
            return [(out,flipflops[node],node) for out in edges[node]]
    elif node in conjunctions:
        wires[node][source]=signal
        out_signal = not all(wires[node].values())
        return [(out, out_signal, node) for out in edges[node]]
    else:
        return [(out,signal,node) for out in edges[node]]

for _ in range(1000):
    Q=deque([("broadcaster",False,"button")])
    while Q:
        state=Q.popleft()
        target,signal,source=state
        for n in neighbors(state):
            Q.append(n)
part1=highs*lows
print("Part 1:", part1)

subcircuits=edges["broadcaster"]
part2=1
for sc in subcircuits:
    cur=sc
    i=0
    tot=0
    while True:
        inbound=[k for k,v in edges.items() if cur in v]
        outbound=[n for n in edges[cur] if n in flipflops]
        if len(inbound)==1:
            tot+=2**i
        if not outbound:
            break
        cur=outbound[0]
        i+=1
    part2*=tot+1

print("Part 2:", part2)


