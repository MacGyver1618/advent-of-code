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

lines = read_lines(24)

R = len(lines)-2
C = len(lines[0])-2
T = sym.lcm(R,C)
blizzards = defaultdict(list)
for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char in "^v<>":
            blizzards[(r-1,c-1)] += char

maze = []
for t in range(T):
    maze.append(blizzards)
    next_blizzards = defaultdict(list)
    for (r,c),ds in blizzards.items():
        for d in ds:
            if d == "^":
                next_blizzards[((r-1)%R,c)] += d
            elif d == "v":
                next_blizzards[((r+1)%R,c)] += d
            elif d == "<":
                next_blizzards[(r,(c-1)%C)] += d
            elif d == ">":
                next_blizzards[(r,(c+1)%C)] += d
    blizzards = next_blizzards

start = (-1,0,0)
def at_end(pos):
    r,c,t = pos
    return (r,c) == (R,C-1)

def at_start(pos):
    r,c,t = pos
    return (r,c) == (-1,0)

def in_bounds(pos):
    r,c,t = pos
    return ((r,c) in ((-1,0),(R,C-1)) or 0 <= r < R and 0 <= c < C) and (r,c) not in maze[t%T]

def neighbor_fn(pos):
    r,c,t = pos
    t += 1
    return [(y,x,t) for (y,x) in ((r,c),(r+1,c),(r-1,c),(r,c+1),(r,c-1)) if in_bounds((y,x,t))]

path = bfs(start, at_end, neighbor_fn)

for p in path:
    pr,pc,t = p
    ss = []
    ss.append("#" + ("E" if (pr,pc) == (-1,0) else ".") + "#"*C)
    for r in range(R):
        s = "#"
        for c in range(C):
            if (r,c) == (pr,pc):
                s += "E"
            elif (r,c) in maze[t%T]:
                l = len(maze[t%T][(r,c)])
                s += maze[t%T][(r,c)][0] if l == 1 else str(l)
            else:
                s += "."
        s += "#"
        ss.append(s)
    ss.append("#"*C + ("E" if (pr,pc) == (R,C) else ".") + "#")
    print("\n".join(ss))
    time.sleep(0.017)


print("Part 1:", len(path)-1)
path2 = bfs(path[-1], at_start, neighbor_fn)
path3 = bfs(path2[-1], at_end, neighbor_fn)
print("Part 2:", len(path+path2+path3)-3)
