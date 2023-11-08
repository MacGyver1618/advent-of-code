import collections

from common.advent_lib import *
import re
import more_itertools as it2
import functools as ft
from collections import defaultdict
import json

inpt = read_lines(22)[2:]

# x y size used avail use%

nodes = set()
coords = set()
capacities = {}

lr = r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%"
for line in inpt:
    node = tuple(map(int, re.match(lr, line).groups()))
    nodes.add(node)
    capacities[node[:2]] = node[2:]

R=max(n[1] for n in nodes)+1
C=max(n[0] for n in nodes)+1
SIZE=0
USED=1
AVAIL=2

grid=defaultdict(tuple)
for n in sorted(nodes):
    c,r,s,u,a,_ = n
    grid[(r,c)]=(s,u,a)

def viable_pairs(ns):
    result = set()
    for a, (_, need, _, used) in ns.items():
        for b, (_, _, avail, _) in ns.items():
            if used > 0 and a != b and avail >= need:
                result.add((a,b))
    return result

print("Part 1:", len(viable_pairs(capacities)))

def neighbor_fn(p):
    r,c=p
    for n in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
        nr,nc=n
        if 0<=nr<R and 0<=nc<C and grid[n][SIZE] < 100:
            yield n

data_pos = (0,C-1)
payload_size = grid[data_pos][USED]
slot_pos = [(r,c) for r in range(R) for c in range(C) if grid[(r,c)][AVAIL] >= payload_size][0]
data_path=[(0,c) for c in range(C-2,-1,-1)]
slot_path=bfs(slot_pos,lambda p: p==data_path[0],neighbor_fn)

print("Part 2:", len(slot_path)+(len(data_path)-1)*5)