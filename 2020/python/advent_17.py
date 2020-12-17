from advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(17)

grid = []

for j,row in enumerate(inpt):
    for i,char in enumerate(row):
        if char == '#':
            grid.append((i,j,0))

def neighbors(p):
    x,y,z = p
    sum = 0
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            for k in range(z-1,z+2):
                if not (i == x and j == y and k == z):
                    if (i, j, k) in grid:
                        sum += 1
    return sum


def printgrid():
    xmin = min([i for (i,j,k) in grid])-1
    xmax = max([i for (i,j,k) in grid])+2
    ymin = min([j for (i,j,k) in grid])-1
    ymax = max([j for (i,j,k) in grid])+2
    zmin = min([k for (i,j,k) in grid])-1
    zmax = max([k for (i,j,k) in grid])+2
    for j in range(ymin,ymax):
        s = ""
        for i in range(xmin,xmax):
            s += '#' if (i,j,0) in grid else '.'
        print(s)
    print()
    for j in range(ymin,ymax):
        s = ""
        for i in range(xmin,xmax):
            s += str(neighbors((i,j,0)))
        print(s)


for _ in range(6):
    nxt = []
    xmin = min([i for (i,j,k) in grid])-1
    xmax = max([i for (i,j,k) in grid])+2
    ymin = min([j for (i,j,k) in grid])-1
    ymax = max([j for (i,j,k) in grid])+2
    zmin = min([k for (i,j,k) in grid])-1
    zmax = max([k for (i,j,k) in grid])+2
    for p in [(x,y,z) for x in range(xmin, xmax) for y in range(ymin,ymax) for z in range(zmin,zmax)]:
        n = neighbors(p)
        if p in grid and 2 <= n <= 3:
            nxt.append(p)
        elif p not in grid and n == 3:
            nxt.append(p)
    grid = nxt

print("Part 1:", len(grid))


grid = []

for j,row in enumerate(inpt):
    for i,char in enumerate(row):
        if char == '#':
            grid.append((i,j,0,0))

def neighbors(p):
    x,y,z,a = p
    sum = 0
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            for k in range(z-1,z+2):
                for l in range(a-1,a+2):
                    if not (i == x and j == y and k == z and l == a):
                        if (i, j, k, l) in grid:
                            sum += 1
    return sum

for _ in range(6):
    nxt = []
    xmin = min([i for (i,j,k,l) in grid])-1
    xmax = max([i for (i,j,k,l) in grid])+2
    ymin = min([j for (i,j,k,l) in grid])-1
    ymax = max([j for (i,j,k,l) in grid])+2
    zmin = min([k for (i,j,k,l) in grid])-1
    zmax = max([k for (i,j,k,l) in grid])+2
    amin = min([l for (i,j,k,l) in grid])-1
    amax = max([l for (i,j,k,l) in grid])+2
    for p in [(x,y,z,a) for x in range(xmin, xmax) for y in range(ymin,ymax) for z in range(zmin,zmax) for a in range(amin,amax)]:
        n = neighbors(p)
        if p in grid and 2 <= n <= 3:
            nxt.append(p)
        elif p not in grid and n == 3:
            nxt.append(p)
    grid = nxt

print("Part 2:", len(grid))
