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

lines = read_lines(20)

grid=[[c for c in line] for line in lines]
R=len(grid)
C=len(grid[0])

outer_left=2
outer_right=C-3
outer_up=2
outer_down=R-3
inner_left=C//2-sum(1 for i in range(C//2,2,-1) if grid[R//2][i] not in "#.")
inner_right=C//2+sum(1 for i in range(C//2,C-2) if grid[R//2][i] not in "#.")
inner_up=R//2-sum(1 for i in range(R//2,2,-1) if grid[i][C//2] not in "#.")
inner_down=R//2+sum(1 for i in range(R//2,R-2) if grid[i][C//2] not in "#.")
portals=defaultdict(list)

def parse_portals(const,varmin,varmax,direction,labels):
    for var in range(varmin,varmax):
        if direction=="vertical":
            if grid[var][const]==".":
                if labels=="before":
                    label=grid[var][const-2]+grid[var][const-1]
                    portals[label]+=[(var, const)]
                elif labels=="after":
                    label=grid[var][const+1]+grid[var][const+2]
                    portals[label]+=[(var, const)]
        elif direction=="horizontal":
            if grid[const][var]==".":
                if labels=="before":
                    label=grid[const-2][var]+grid[const-1][var]
                    portals[label]+=[(const, var)]
                elif labels=="after":
                    label=grid[const+1][var]+grid[const+2][var]
                    portals[label]+=[(const, var)]

parse_portals(outer_up,outer_left,outer_right+1,"horizontal","before")
parse_portals(outer_down,outer_left,outer_right+1,"horizontal","after")
parse_portals(outer_left,outer_up,outer_down+1,"vertical","before")
parse_portals(outer_right,outer_up,outer_down+1,"vertical","after")
parse_portals(inner_up,inner_left,inner_right+1,"horizontal","after")
parse_portals(inner_down,inner_left,inner_right+1,"horizontal","before")
parse_portals(inner_left,inner_up,inner_down+1,"vertical","after")
parse_portals(inner_right,inner_up,inner_down+1,"vertical","before")

portal_points=[p for portal in portals.values() for p in portal]

def neighbor_fn(p):
    if p in portal_points:
        for n in [n for portal in portals.values() for n in portal if p in portal]:
            if n!=p:
                yield n
    for n in adjacent(p):
        r,c=n
        if grid[r][c]==".":
            yield tuple(n)


path=bfs(portals["AA"][0], eq(portals["ZZ"][0]), neighbor_fn)
part1 = len(path)-1
print("Part 1:", part1)

def neighbor_fn2(p):
    *p,level = p
    p=tuple(p)
    if p in portal_points:
        for n in [n for portal in portals.values() for n in portal if p in portal]:
            r,c=n
            if n!=p:
                if (r in (outer_up,outer_down) or c in (outer_left,outer_right)):
                    yield r,c, level + 1
                elif level>0:
                    yield r,c, level - 1

    for n in adjacent(p):
        r,c=n
        if grid[r][c]==".":
            yield r,c, level

path2=a_star((*(portals["AA"][0]),0), eq((*(portals["ZZ"][0]),0)), neighbor_fn2,lambda _,_2:1,lambda p: manhattan_distance(p[:2],portals["ZZ"][
    0])+1000*p[2])

part2 = len(path2)-1
print("Part 2:", part2)
