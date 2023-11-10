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

lines = read_lines(16)
Q=deque("abcdefghijklmnop")
for instr in lines[0].split(","):
    op=instr[0]
    rest=instr[1:]
    if op=="s":
        Q.rotate(int(rest))
    elif op=="x":
        a,b=map(int,rest.split("/"))
        t=Q[b]
        Q[b]=Q[a]
        Q[a]=t
    elif op=="p":
        a,b=rest.split("/")
        i=Q.index(a)
        j=Q.index(b)
        t=Q[j]
        Q[j]=Q[i]
        Q[i]=t

part1 = "".join(Q)
print("Part 1:", part1)

Q=deque("abcdefghijklmnop")
cycle_found=False
history=["abcdefghijklmnop"]
iters=0
while not cycle_found:
    for pos,instr in enumerate(lines[0].split(",")):
        # state = (pos,tuple(Q))
        # if state in history:
        #     cycle_found = True
        #     cycle_length = len(history)-history.index(state)
        #     tail_length = len(history)-cycle_length
        #     break
        # else:
        #     history += [state]
        # if len(history)%1000 == 0:
        #     print(len(history))
        op=instr[0]
        rest=instr[1:]
        if op=="s":
            Q.rotate(int(rest))
        elif op=="x":
            a,b=map(int,rest.split("/"))
            t=Q[b]
            Q[b]=Q[a]
            Q[a]=t
        elif op=="p":
            a,b=rest.split("/")
            i=Q.index(a)
            j=Q.index(b)
            t=Q[j]
            Q[j]=Q[i]
            Q[i]=t
    state = "".join(Q)
    if state=="abcdefghijklmnop":
        cycle_found=True
    else:
        history += [state]
    iters+=1

part2 = history[1_000_000_000%iters]
print("Part 2:", part2)
