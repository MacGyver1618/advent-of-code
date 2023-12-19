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

lines = read_lines(18)
dirs={
"R":1,
"D":1j,
"L":-1,
"U":-1j
}
grid={}

pos=0
for line in lines:
    _dir,steps,color=line.split()
    color=int(color[2:-1],16)
    for _ in range(int(steps)):
        pos+=dirs[_dir]
        grid[pos]=color

cmin=min(int(p.real) for p in grid)
cmax=max(int(p.real) for p in grid)
rmin=min(int(p.imag) for p in grid)
rmax=max(int(p.imag) for p in grid)

rmid=(rmin+rmax)//2
cmid=(cmin+cmax)//2
inside=bfs(cmid+1j*rmid,lambda _:False,lambda p: [p+d for d in dirs.values() if p+d not in grid])

part1 = len(grid)+len(inside)
print("Part 1:", part1)

points=[0]
cur=0
border=0
for line in lines:
    cc=re.findall(r"\w{6}",line)[0]
    l=int(cc[:5],16)
    _dir=[*dirs.values()][int(cc[-1])]
    cur+=l*_dir
    border+=l
    points+=[cur]

def unpack(p):
    return map(int,[p.real,p.imag])

part2 = (sum(y2*x1-y1*x2 for (x1,y1),(x2,y2) in zip(map(unpack,points[:-1]),map(unpack,points[1:])))+border)//2+1
print("Part 2:", part2)
