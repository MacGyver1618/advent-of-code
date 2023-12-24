import fractions

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
import scipy

lines = read_lines(24)

hail=[]
for line in lines:
    px,py,pz,vx,vy,vz=map(int,re.findall(r"-?\d+", line))
    hail+=[(px,py,pz,vx,vy,vz)]

part1 = 0
LO,HI=200000000000000,400000000000000

def p2l(h):
    px,py,_,vx,vy,_=h
    a=fractions.Fraction(vy,vx)
    c=py-a*px
    return a,c

for i in range(len(hail)):
    a,c=p2l(hail[i])
    for j in range(i+1,len(hail)):
        b,d=p2l(hail[j])
        if a==b:
            continue
        ix=(d-c)/(a-b)
        iy=a*ix+c
        ta=(ix-hail[i][0])/hail[i][3]
        tb=(ix-hail[j][0])/hail[j][3]
        if ix and LO <= ix <= HI and LO <= iy <= HI and ta > 0 and tb > 0:
            part1+=1

print("Part 1:", part1)

px=sym.Symbol("px")
py=sym.Symbol("py")
pz=sym.Symbol("pz")
vx=sym.Symbol("vx")
vy=sym.Symbol("vy")
vz=sym.Symbol("vz")

eqs=[]
ts=[]
for i,h in enumerate(hail[:3]):
   pxh,pyh,pzh,vxh,vyh,vzh=h
   t=sym.Symbol(f"t{i}")
   eqx=px+vx*t-pxh-vxh*t
   eqy=py+vy*t-pyh-vyh*t
   eqz=pz+vz*t-pzh-vzh*t
   eqs+=[eqx,eqy,eqz]
   ts+=[t]

solved=sym.solve_poly_system(eqs,*([px,py,pz,vx,vy,vz]+ts))
part2=sum(solved[0][:3])
print("Part 2:", part2)
