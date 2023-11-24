from intcode import IntCodeMachine
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

program=[*map(int,read_lines(11)[0].split(","))]
grid=defaultdict(int)
machine = IntCodeMachine(program)
pos=0
_dir=-1j
while not machine.finished():
    machine.input(grid[pos])
    machine.run()
    grid[pos]=machine.read()
    _dir *= [-1j,1j][machine.read()]
    pos+=_dir

part1 = len(grid)
print("Part 1:", part1)

grid=defaultdict(int)
grid[0]=1
machine = IntCodeMachine(program)
pos=0
_dir=-1j
while not machine.finished():
    machine.input(grid[pos])
    machine.run()
    grid[pos]=machine.read()
    _dir *= [-1j,1j][machine.read()]
    pos+=_dir

print("Part 2:")
rmin=int(min(p.imag for p in grid))
rmax=int(max(p.imag for p in grid))
cmin=int(min(p.real for p in grid))
cmax=int(max(p.real for p in grid))
for r in range(rmin,rmax+1):
    s=""
    for c in range(cmin,cmax+1):
        s+="#" if grid[c+1j*r] else " "
    print(s)