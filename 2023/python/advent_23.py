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

lines = read_lines(23)
R = len(lines)
C = len(lines[0])

def char_at(p):
    r=int(p.imag)
    c=int(p.real)
    return lines[r][c]

def in_bounds(p):
    r=int(p.imag)
    c=int(p.real)
    return 0<=r<R and 0<=c<C

def nc(p):
    return len([p+d for d in [1,-1,1j,-1j] if in_bounds(p+d) and char_at(p+d) != "#"])


ends=[]
branches=[]

for r in range(R):
    for c in range(C):
        p=c+1j*r
        if lines[r][c]!="#":
            ns=nc(p)
            if ns==1:
                ends+=[p]
            elif ns>2:
                branches+=[p]

nodes=[*ends,*branches]

Ds={
    ">":1,
    "<":-1,
    "^":-1j,
    "v":1j
}

def neighbors(p,target):
    char = char_at(p)
    if char in Ds:
        n=p+Ds[char]
        if n not in nodes or n==target:
            return [n]
        else:
            return []
    else:
        return [p+d for d in [1,-1,1j,-1j] if in_bounds(p+d) and char != "#" and (p+d not in nodes or p+d==target)]


G1=defaultdict(list)
for i,a in enumerate(nodes):
    for j,b in enumerate(nodes):
        if i==j:
            continue
        path=bfs(a,eq(b),lambda p: neighbors(p, b))
        if isinstance(path,list):
            G1[i]+=[(j, len(path) - 1)]
print(G1)

dist=defaultdict(lambda:float("-inf"))

def neighbors2(state):
    p,seen,l=state
    if l>dist[p]:
        dist[p]=l
    if p==1:
        return []
    return [(n,seen|{n},l+d) for n,d in G1[p] if n not in seen]


start=(0,frozenset({0}),0)
Q=deque()
Q.append(start)
while Q:
    cur=Q.popleft()
    for n in neighbors2(cur):
        Q.append(n)
part1=dist[1]
print("Part 1:", part1)

G2=defaultdict(list)
for i,a in enumerate(nodes):
    for j,b in enumerate(nodes):
        if i==j:
            continue
        path=bfs(a,eq(b),lambda p: [p+d for d in [1,-1,1j,-1j] if in_bounds(p+d) and char_at(p+d) != "#" and (p+d not in nodes or p+d==b)])
        if isinstance(path,list):
            G2[i]+=[(j, len(path) - 1)]
print(G2)

def neighbors3(state):
    p,seen,l=state
    if l>dist[p]:
        dist[p]=l
        if p==1:
            print (ml)
    if p==1:
        return []
    return [(n,seen|{n},l+d) for n,d in G2[p] if n not in seen]

dist=defaultdict(lambda:float("-inf"))
ml=0
start=(0, frozenset({0}),0)
Q=deque()
Q.append(start)
while Q:
    ml=max(ml,len(Q))
    cur=Q.popleft()
    #sys.stdout.write(f"\r{dist[p]} {len(Q)}")
    for n in neighbors3(cur):
        Q.append(n)

part2=dist[1]
#sys.stdout.write("\r")
print(ml)
print("Part 2:", part2)
