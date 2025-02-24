import concurrent.futures

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

lines = read_lines(24)
R = len(lines)
C = len(lines[0])

regs={}
edges=set()
gates=set()
counts=defaultdict(int)

def dotify(a,op,b,target):
    print(f"{a}->{op}{counts[op]}")
    print(f"{b}->{op}{counts[op]}")
    print(f"{op}{counts[op]}->{target}")
    counts[op]+=1


for line in lines:
    if ":" in line:
        regs[line[:3]]= int(line[5])
    elif "->" in line:
        a,op,b,_,target = line.split()
        # dotify(a,op,b,target)
        edges.add((a,target))
        edges.add((b,target))
        gates.add((a, op, b, target))


# input()

def run(rules):
    Q=deque(rules)
    regs2=regs.copy()
    time_since=len(Q)
    while Q:
        if not time_since:
            return None
        a,op,b,target=Q.popleft()
        if a in regs2 and b in regs2:
            time_since=len(Q)
            if op == "AND":
                regs2[target]=regs2[a]&regs2[b]
            elif op == "OR":
                regs2[target]=regs2[a]|regs2[b]
            elif op == "XOR":
                regs2[target]=regs2[a]^regs2[b]
        else:
            time_since-=1
            Q.append((a,op,b,target))
    return sum(regs2[reg]<<i for i,reg in enumerate(sorted(reg for reg in regs2 if reg.startswith("z")))),regs2

part1,regs_after = run(gates)
print("Part 1:", part1)

x=sum(regs[reg]<<i for i,reg in enumerate(sorted(reg for reg in regs if reg.startswith("x"))))
y=sum(regs[reg]<<i for i,reg in enumerate(sorted(reg for reg in regs if reg.startswith("y"))))
z=sum(regs[reg]<<i for i,reg in enumerate(sorted(reg for reg in regs if reg.startswith("z"))))

print(f"x: {x:046b}")
print(f"y: {y:046b}")
print(f"z: {z:046b}")
print(f"Z: {x+y:046b}")
print(f"d: {(x+y)^z:046b}")

import networkx as nx
G=nx.DiGraph(edges)
incorrect=set()
for reg in sorted(regs_after):
    if reg.startswith("z"):
        pos=int(reg[1:])
        mask=1<<pos
        if (x+y)&mask!=(regs_after[reg]<<pos):
            incorrect.add(reg)

possibles=set()

paths_to_bit=defaultdict(list)
for a in incorrect:
    for b in sorted(reg for reg in regs_after if reg[0] in "xy"):
        paths_to_bit[a]+=[*nx.all_simple_paths(G,b,a)]

g1 = intersection(union(paths_to_bit[b]) for b in ["z06","z07","z08"])
g2 = intersection(union(paths_to_bit[b]) for b in ["z11","z12","z13","z14"])
g3 = intersection(union(paths_to_bit[b]) for b in ["z23","z24","z25","z26"])
print(len(g1))
print(len(g2))
print(len(g3))
swaps=[n for n in intersection([g1,g2,g3]) if n[0] not in "xy"]

def swap(a,b,source):
    rules=set()
    for gate in source:
        if gate[-1]==a:
            rules.add((*gate[:-1],b))
        elif gate[-1]==b:
            rules.add((*gate[:-1],a))
        else:
            rules.add(gate)
    return rules
gates=swap("dhg","z06",gates)
gates=swap("nbf","z38",gates)
# #r2=swap("bcg","hpg",source=r1)
gates=swap("brk","dpd",gates)
gates=swap("z23","bhd",gates)
print(",".join(sorted(["dhg","z06","nbf","z38","brk","dpd","z23","bhd"])))
input()
res,_=run(gates)
expected=f"{x+y:046b}"
actual=f"{res:046b}"
print(f"z: {expected}")
print(f"z: {''.join(f'\033[{37 if c==expected[i] else 31}m{c}\033[39m' for i,c in enumerate(actual))}")
input()
for rule in sorted(gates):
    dotify(*rule)
input()
for a,b in it.combinations(swaps,2):
    print(f"swapping {a} and {b}")
    vals=run(swap(a,b,gates))
    if vals:
        z=vals[0]
        expected=f"{x+y:046b}"
        actual=f"{z:046b}"
        print(f"z: {expected}")
        print(f"z: {''.join(f'\033[{37 if c==expected[i] else 31}m{c}\033[39m' for i,c in enumerate(actual))}")
        input()
    else:
        print(f"swapping {a} and {b} timed out!")
        input()

part2 = 0
print("Part 2:", part2)
