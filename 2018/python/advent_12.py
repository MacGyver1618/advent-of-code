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
state=set()
for i,c in enumerate(lines[0].split()[-1]):
    if c=='#':
        state.add(i)
rules=dict()
for line in lines[2:]:
    a,b=line.split(" => ")
    rules[a]=b

def iterate(state):
    global generations,history
    next_state=set()
    for i in range(min(state)-4, max(state)+5):
        vicinity="".join("#" if p in state else "." for p in range(i-2,i+3))
        if rules[vicinity] == "#":
            next_state.add(i)
    return next_state

def normalized(state):
    return set(p-min(state) for p in state)

history=[]
offsets=[]
generations=0

for _ in range(20):
    state=iterate(state)
    generations+=1
    history.append(normalized(state))
    offsets.append(min(state))

part1 = sum(state)
print("Part 1:", part1)

while True:
    state=iterate(state)
    generations+=1
    offsets.append(min(state))
    if normalized(state) in history:
        break
    history.append(normalized(state))


offset=offsets[-1]
travel=offset-offsets[-2]
part2=sum(p+offset+travel*(50_000_000_000-generations) for p in normalized(state))
print("Part 2:", part2)
