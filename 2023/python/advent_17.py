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

lines = read_lines(17)
R=len(lines)
C=len(lines[0])
grid= {}
for r,line in enumerate(lines):
    for c,char in enumerate(line):
        pos=c+r*1j
        grid[pos]=int(char)

def neighbors(state):
    pos,_dir,steps_in_direction=state
    if steps_in_direction < 3 and pos+_dir in grid:
        yield pos+_dir,_dir,steps_in_direction+1
    for turn in 1j,-1j:
        new_dir=_dir*turn
        if pos+new_dir in grid:
            yield pos+new_dir,new_dir,1


path = list(dijkstra((0,1,0),lambda s: s[0]==(R-1)*1j+C-1, neighbors, lambda _,s:grid[s[0]]))
part1=sum(grid[s[0]] for s in path[1:])
print("Part 1:", part1)

def neighbors2(state):
    pos,_dir,steps_in_direction=state
    if steps_in_direction < 10 and pos+_dir in grid:
        yield pos+_dir,_dir,steps_in_direction+1
    if steps_in_direction >= 4:
        for turn in 1j,-1j:
            new_dir=_dir*turn
            if pos+new_dir in grid:
                yield pos+new_dir,new_dir,1

path = list(dijkstra((0,1,0),lambda s: s[0]==(R-1)*1j+C-1 and 4<=s[2]<=10, neighbors2, lambda _,s:grid[s[0]]))
part2=sum(grid[s[0]] for s in path[1:])

print("Part 2:", part2)
