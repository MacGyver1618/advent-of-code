import time

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

from intcode import IntCodeMachine

machine = IntCodeMachine.from_day_input(13)

grid=defaultdict(int)

machine.run()
def read_state():
    try:
        while True:
            x=machine.read()
            y=machine.read()
            tile_id=machine.read()
            grid[(y,x)]=tile_id
    except Exception:
        pass

read_state()
part1 = list(grid.values()).count(2)
print("Part 1:", part1)

rmin=min(r for r,c in grid)
rmax=max(r for r,c in grid)
cmin=min(c for r,c in grid)
cmax=max(c for r,c in grid)

def print_grid():
    ss=[]
    for r in range(rmin,rmax+1):
        s=""
        for c in range(cmin,cmax+1):
            s+=" |#-*"[grid[r,c]]
        ss+=[s]
    print("\n".join(ss))

machine = IntCodeMachine.from_day_input(13)
machine.set_val(0,2)
machine.run()
while not machine.finished():
    read_state()
    # print_grid()
    # time.sleep(1/30)
    ball_x=[c for (r,c),v in grid.items() if v==4][0]
    padl_x=[c for (r,c),v in grid.items() if v==3][0]
    machine.input(sgn(ball_x-padl_x))
    machine.run()
try:
    while True:
        part2=machine.read()
except Exception:
    pass
print("Part 2:", part2)
