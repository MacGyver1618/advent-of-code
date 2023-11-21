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
from functools import lru_cache

lines = read_lines(22)
depth=int(lines[0].split()[-1])
x,y=map(int,lines[1].split()[-1].split(","))
target=(y,x)

@lru_cache(maxsize=None)
def geo_index(r,c):
    if (r,c)==(0,0) or (r,c)==(y,x):
        return 0
    if r==0:
        return c*16807
    if c==0:
        return r*48271
    return erosion_level(r,c-1)*erosion_level(r-1,c)

@lru_cache(maxsize=None)
def erosion_level(r,c):
    return (geo_index(r,c)+depth) % 20183

def terrain_type(r,c):
    return erosion_level(r,c)%3

part1 = sum(terrain_type(r,c) for c in range(x+1) for r in range(y+1))
print("Part 1:", part1)

ROCKY,WET,NARROW=0,1,2
NEITHER,TORCH,GEAR=0,1,2
pos=(0,0,TORCH)

def neighbor_fn(p):
    r,c,current_equipment=p
    current_terrain=terrain_type(r,c)
    for new_equipment in [TORCH,GEAR,NEITHER]:
        if new_equipment != current_equipment and new_equipment != current_terrain:
            yield r,c,new_equipment
    for nr,nc in (r+1,c),(r-1,c),(r,c+1),(r,c-1):
        if nr >= 0 and nc >= 0:
            neighbor_terrain = terrain_type(nr,nc)
            if neighbor_terrain != current_equipment:
                yield nr,nc,current_equipment

def distance_fn(a,b):
    *_,ea=a
    *_,eb=b
    if ea != eb:
        return 7
    else:
        return 1

# warm up lru_cache
#
# for r in range(depth):
#     if r%100==0:
#         print(r)
#     for c in range(depth):
#         geo_index(r,c)
# print("cache warm")

def finished(p):
    return p == (y,x,TORCH)

path = dijkstra(pos, finished, neighbor_fn, distance_fn)
time_taken=0

prev = path[0]
for cur in list(path)[1:]:
    r,c,e=cur
    equipment=["NEITHER","TORCH","GEAR"][e]
    terrain=["ROCKY","WET","NARROW"][terrain_type(r,c)]
    time_taken += distance_fn(cur,prev)
    prev=cur
part2 = time_taken
print("Part 2:", part2)
