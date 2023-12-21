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

lines = read_lines(21)
R=len(lines)
C=len(lines[0])

elf=-1
for r in range(R):
    for c in range(C):
        if lines[r][c]=="S":
            elf=c+1j*r

def char_at(p):
    r=int(p.imag)
    c=int(p.real)
    return lines[r][c]

def in_bounds(p):
    return 0<=p.imag<R and 0<=p.real<C

def populate(start,turns):
    poss={start}
    for _ in range(turns):
        poss={p+d for d in [1,-1,1j,-1j] for p in poss if in_bounds(p+d) and char_at(p+d)!="#"}
    return len(poss)

part1=populate(elf,64)
print("Part 1:", part1)

def char_at2(p):
    r=int(p.imag)%R
    c=int(p.real)%C
    return lines[r][c]

def constrain(p):
    r=int(p.imag)%R
    c=int(p.real)%C
    return c+1j*r

S=26501365
M=R//2  # midpoint
T=(S-M)//R # tile count

cycles=defaultdict(list)

pb=ProgressBar(9)
for r in [0,1,2]:
    for c in [0,1,2]:
        pb.update()
        start = M*c + M*r*1j
        cur={start}
        history=[]
        while cur not in history:
            history+=[cur]
            cur={p+d for d in [1,-1,1j,-1j] for p in cur if in_bounds(p+d) and char_at(p+d)!="#"}
        cycles[(r,c)]=[len(s) for s in history]
pb.clear()

part2=cycles[(1,1)][-2:][-2] # cycle[0] is initial state i.e. zero steps taken

for i in range(1,T):
    if i%2==1:
        part2+=4*i*cycles[(0,1)][-1]
    else:
        part2+=4*i*cycles[(0,1)][-2]
E=M+1+(T-1)*R # time to escape fully populated tiles
P=S-E # phase at step count

for r in range(3):
    for c in range(3):
        if (r,c)==(1,1):
            continue
        if (r+c)%2==1: # midpoint
            part2+=cycles[r,c][P]
        else: # corner
            part2+=T*cycles[r,c][P-M-1] # single corner
            part2+=(T-1)*cycles[r,c][P-M-1+R] # missing corner
print("Part 2:", part2)
