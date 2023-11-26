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

grid=[[c for c in line] for line in lines]
R=len(grid)
C=len(grid[0])

specials=[(r,c,grid[r][c]) for r in range(R) for c in range(C) if grid[r][c] not in ".#"]
doors=[s for s in specials if s[2] in ABC]
keys=[s for s in specials if s[2] in abc]
door=[s[:2] for s in specials if s[2]=="@"][0]

shortest_paths={}

for start in abc+"@":
    for end in abc+"@":
        if start==end or (start,end) in shortest_paths:
            continue
        startpos=[s[:2] for s in specials if s[2]==start][0]
        endpos=[s[:2] for s in specials if s[2]==end][0]
        path=bfs(startpos,eq(endpos),lambda p: [tuple(n) for n in adjacent(p) if grid[n[0]][n[1]] != "#"])
        required_keys= {grid[r][c].lower() for r,c in path if grid[r][c] in ABC}
        shortest_paths[start,end]=(path,required_keys)
        shortest_paths[end,start]=(path,required_keys)
        print(start,end)

def neighbor_fn(state):
    pos,keys=state
    print("".join(sorted(keys)))
    return [(c,keys.union({c})) for c in abc if c not in keys and all(key in keys for key in shortest_paths[pos,c][1])]

def dist_fn(a,b):
    return len(shortest_paths[(a[0],b[0])][0])-1

path = dijkstra(("@", frozenset()), lambda state: state[1]==set(abc), neighbor_fn, dist_fn)
path=list(path)
part1 = sum(map(lambda z: dist_fn(*z), zip(path[1:],path[:-1])))
print("Part 1:", part1)

r,c=door
grid[r][c]="#"
grid[r][c+1]="#"
grid[r][c-1]="#"
grid[r+1][c]="#"
grid[r-1][c]="#"
grid[r+1][c+1]="1"
grid[r+1][c-1]="2"
grid[r-1][c+1]="3"
grid[r-1][c-1]="4"

specials=[(r,c,grid[r][c]) for r in range(R) for c in range(C) if grid[r][c] not in ".#"]
shortest_paths={}
for start in abc+"1234":
    for end in abc:
        if start==end or (start,end) in shortest_paths:
            continue
        startpos=[s[:2] for s in specials if s[2]==start][0]
        endpos=[s[:2] for s in specials if s[2]==end][0]
        path=bfs(startpos,eq(endpos),lambda p: [tuple(n) for n in adjacent(p) if grid[n[0]][n[1]] != "#"])
        if isinstance(path,deque):
            required_keys= {grid[r][c].lower() for r,c in path if grid[r][c] in ABC}
            shortest_paths[start,end]=(path,required_keys)
            shortest_paths[end,start]=(path,required_keys)
            print(start,end)

def neighbor_fn2(state):
    poss,keys=state
    print("".join(sorted(keys)))
    for pos in poss:
        for c in abc:
            if c not in keys and (pos,c) in shortest_paths and all(key in keys for key in shortest_paths[pos,c][1]):
                yield poss.replace(pos,c),keys.union({c})

def dist_fn2(a,b):
    start=[c for c in a[0] if c not in b[0]][0]
    end=[c for c in b[0] if c not in a[0]][0]
    return len(shortest_paths[(start,end)][0])-1

path = dijkstra(("1234", frozenset()), lambda state: state[1]==set(abc), neighbor_fn2, dist_fn2)
path=list(path)
part2 = sum(map(lambda z: dist_fn2(*z), zip(path[1:],path[:-1])))
print("Part 2:", part2)
