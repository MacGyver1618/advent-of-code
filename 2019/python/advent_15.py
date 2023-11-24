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

machine = IntCodeMachine.from_day_input(15)
grid= {}
dirs=[0,-1j,1j,-1,1]
tiles="# O"

pos=0
grid[pos]=" "
seen = set()
Q=deque([(0,d) for d in dirs[-1:0:-1]])

def print_grid():
    ss=[]
    for r in range(-21,20):
        s=""
        for c in range(-21,20):
            p=c+1j*r
            if p==pos:
                s+="D"
            elif p in grid:
                s+=grid[c+1j*r]
            else:
                s+="?"
        ss+=[s]
    print("\n".join(ss))

# print_grid()
while Q:
    cur,_dir = Q.pop()
    path=bfs(pos,eq(cur),lambda p: [p+d for d in dirs[1:] if p+d in grid and grid[p+d]!="#"])
    if len(path)>1:
        for i in range(1,len(path)):
            diff = path[i] - path[i - 1]
            machine.input(dirs.index(diff))
            pos+=diff
            # print_grid()
            # time.sleep(1/24)
            machine.run()
            machine.read() # ignore result, we know it's already a blank
    pos=cur
    machine.input(dirs.index(_dir))
    machine.run()
    result=machine.read()
    if result != 0:
        pos+=_dir
    grid[cur+_dir]=tiles[result]
    # print_grid()
    # time.sleep(1/24)
    for d in dirs[1:][::-1]:
        if pos+d not in grid and (pos,d) not in seen:
            Q.append((pos,d))
            seen.add((pos,d))

oxygen_machine=[k for k,v in grid.items() if v=="O"][0]
path=bfs(0,eq(oxygen_machine),lambda p: [p+d for d in dirs[1:] if p+d in grid and grid[p+d]!="#"])
part1 = len(path)-1
print("Part 1:", part1)

minutes=0
Q=deque([oxygen_machine])
pos=float("inf")
# print_grid()
# time.sleep(1/10)
while " " in grid.values():
    fringe = set()
    while Q:
        cur=Q.popleft()
        for n in [cur+d for d in dirs[1:] if grid[cur+d]==" "]:
            fringe.add(n)
    for tile in fringe:
        grid[tile] = "O"
    # print_grid()
    # time.sleep(1/10)
    Q.extend(fringe)
    minutes += 1

part2=minutes
print("Part 2:", part2)
