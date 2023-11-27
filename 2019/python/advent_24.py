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
import sys

original_grid = [[c for c in line] for line in read_lines(24)]
history=[original_grid]

def next_gen(state):
    next_state=[["."]*5 for _ in range(5)]
    for r in range(5):
        for c in range(5):
            tile=state[r][c]
            bugs= sum(1 for r1,c1 in adjacent((r,c)) if 0<=r1<5 and 0<=c1<5 and state[r1][c1]=="#")
            if tile=="#":
                next_state[r][c]="#" if bugs == 1 else "."
            else:
                next_state[r][c]="#" if bugs in (1,2) else "."
    return next_state

grid=original_grid
while True:
    grid=next_gen(grid)
    if grid in history:
        break
    history+=[grid]

part1 = sum(2**i if c=="#" else 0 for i,c in enumerate(c for line in grid for c in line))
print("Part 1:", part1)



def empty_grid():
    return [["."] * 5 for _ in range(5)]

state=[empty_grid(),original_grid,empty_grid()]
def spinning_cursor():
    while True:
        for cursor in "-\\|/":
            yield cursor
def print_grids(state):
    for d in range(len(state)):
        print(f"Depth {-(len(state)//2)+d}")
        for r in range(5):
            s=""
            for c in range(5):
                s+="?" if (r,c)==(2,2) else state[d][r][c]
            print(s)
        print()

EMPTY=empty_grid()
spin_iter=spinning_cursor()
sys.stdout.write(next(spin_iter))
for i in range(200):
    sys.stdout.write("\r")
    sys.stdout.write(next(spin_iter))
    sys.stdout.flush()
    next_state=[empty_grid() for _ in range(len(state))]
    L=len(next_state)
    for d in range(L):
        for r in range(5):
            for c in range(5):
                if (r,c)==(2,2):
                    continue
                bugs=sum(1 for r1,c1 in adjacent((r,c)) if 0<=r1<5 and 0<=c1<5 and state[d][r1][c1]=="#")
                if d>0:
                    if r==0:
                        bugs+=1 if state[d-1][1][2]=="#" else 0
                    if r==4:
                        bugs+=1 if state[d-1][3][2]=="#" else 0
                    if c==0:
                        bugs+=1 if state[d-1][2][1]=="#" else 0
                    if c==4:
                        bugs+=1 if state[d-1][2][3]=="#" else 0
                if d<L-1:
                    if (r,c)==(1,2):
                        bugs+=sum(1 for i in range(5) if state[d+1][0][i]=="#")
                    if (r,c)==(2,1):
                        bugs+=sum(1 for i in range(5) if state[d+1][i][0]=="#")
                    if (r,c)==(2,3):
                        bugs+=sum(1 for i in range(5) if state[d+1][i][4]=="#")
                    if (r,c)==(3,2):
                        bugs+=sum(1 for i in range(5) if state[d+1][4][i]=="#")
                tile=state[d][r][c]
                if tile=="#":
                    next_state[d][r][c]="#" if bugs == 1 else "."
                else:
                    next_state[d][r][c]="#" if bugs in (1,2) else "."
    if next_state[0]!=EMPTY:
        next_state=[empty_grid(),*next_state]
    if next_state[-1]!=EMPTY:
        next_state=[*next_state,empty_grid()]
    state=next_state

sys.stdout.write("\r")
sys.stdout.flush()


part2=sum(1 for grid in state for line in grid for cell in line if cell=="#")
print("Part 2:", part2)
