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

lines = read_lines(13)
grid=defaultdict(lambda:" ")
R=len(lines)
C=len(lines[0])
carts=[]
for r,line in enumerate(lines):
    for c,char in enumerate(line):
        pos=c+r*1j
        if char in r"/\-|+":
            grid[pos]=char
        elif char == "<":
            carts.append((pos,-1,0))
            grid[pos]="-"
        elif char == ">":
            carts.append((pos,1,0))
            grid[pos]="-"
        elif char == "^":
            carts.append((pos,-1j,0))
            grid[pos]="|"
        elif char == "v":
            carts.append((pos,1j,0))
            grid[pos]="|"

part1=None
while True:
    carts=sorted(carts,key=lambda c:(c[0].imag,c[0].real))
    for i,cart in enumerate(carts):
        pos,d,turns=cart
        pos+=d
        collisions=[(j,cart2) for j,cart2 in enumerate(carts) if cart2[0]==pos and cart2!=cart]
        if collisions:
            if not part1:
                part1=pos
            carts[i]=0,0,0
            for collision in collisions:
                j,cart2=collision
                carts[j]=0,0,0
            continue
        c=grid[pos]
        if c=="\\":
            d*=-1j if d.real==0 else 1j
        elif c=="/":
            d*=-1j if d.imag==0 else 1j
        elif c=="+":
            d*=[-1j,1,1j][turns%3]
            turns+=1
        carts[i]=pos,d,turns
    carts=[cart for cart in carts if cart[1]!=0]
    if len(carts)==1:
        break

print("Part 1:", f"{part1.real:.0f},{part1.imag:.0f}")
part2=carts[0][0]
print("Part 2:", f"{part2.real:.0f},{part2.imag:.0f}")
