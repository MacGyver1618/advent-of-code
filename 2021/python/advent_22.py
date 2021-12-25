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

inpt = lines(22)

on = set()

for i, line in enumerate(inpt):
    gs = re.match(r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line).groups()
    mode = gs[0]
    xmin,xmax,ymin,ymax,zmin,zmax = map(int, gs[1:])
    for x in range(max(xmin,-50), min(51,xmax+1)):
        for y in range(max(ymin, -50), min(51, ymax+1)):
            for z in range(max(zmin,-50), min(zmax+1, 51)):
                if mode == "on":
                    on.add((x,y,z))
                elif (x,y,z) in on:
                    on.remove((x,y,z))

part1 = len(on)
print("Part 1:", part1)

def sizeof(region):
    xmin, xmax, ymin, ymax, zmin, zmax = region
    return (xmax-xmin+1)*(ymax-ymin+1)*(zmax-zmin+1)

def split(region, other):
    xmin1,xmax1,ymin1,ymax1,zmin1,zmax1 = region
    xmin2,xmax2,ymin2,ymax2,zmin2,zmax2 = other
    result = []
    x_intersect = xmin1 <= xmax2 and xmax1 >= xmin2
    y_intersect = ymin1 <= ymax2 and ymax1 >= ymin2
    z_intersect = zmin1 <= zmax2 and zmax1 >= zmin2
    if not (x_intersect and y_intersect and z_intersect):
        result.append(region)
        return result
    if xmin1 < xmin2:
        result.append((xmin1,xmin2-1,ymin1,ymax1,zmin1,zmax1))
        xmin1 = xmin2
    if xmax1 > xmax2:
        result.append((xmax2+1,xmax1,ymin1,ymax1,zmin1,zmax1))
        xmax1 = xmax2
    if ymin1 < ymin2:
        result.append((xmin1,xmax1,ymin1,ymin2-1,zmin1,zmax1))
        ymin1 = ymin2
    if ymax1 > ymax2:
        result.append((xmin1,xmax1,ymax2+1,ymax1,zmin1,zmax1))
        ymax1 = ymax2
    if zmin1 < zmin2:
        result.append((xmin1,xmax1,ymin1,ymax1,zmin1,zmin2-1))
    if zmax1 > zmax2:
        result.append((xmin1,xmax1,ymin1,ymax1,zmax2+1,zmax1))
    return result

def size_of_intersection(a, b):
    xmin1,xmax1,ymin1,ymax1,zmin1,zmax1 = a
    xmin2,xmax2,ymin2,ymax2,zmin2,zmax2 = b
    x_intersect = xmin1 <= xmax2 and xmax1 >= xmin2
    y_intersect = ymin1 <= ymax2 and ymax1 >= ymin2
    z_intersect = zmin1 <= zmax2 and zmax1 >= zmin2
    if not (x_intersect and y_intersect and z_intersect):
        return 0
    return (min(xmax1,xmax2)-max(xmin1, xmin2)+1)*(min(ymax1,ymax2)-max(ymin1, ymin2)+1)*(min(zmax1,zmax2)-max(zmin1, zmin2)+1)

print(size_of_intersection((1,3,1,3,1,3),(2,4,2,4,2,4)))

regions = []
on_count = 0

for line in inpt:
    mode, *rest = re.match(r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line).groups()
    region = tuple(map(int, rest))
    for other in regions:
        on_count -= size_of_intersection(region, other)
    if mode == "on":
        on_count += sizeof(region)
        regions.append(region)

for line in inpt:
    mode, *rest = re.match(r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line).groups()
    region = tuple(map(int, rest))
    new_regions = []
    for other in regions:
        splits = split(other, region)
        new_regions += splits
    if mode == "on":
        new_regions.append(region)
    regions = new_regions

print(on_count)
part2 = sum(map(sizeof, regions))
print("Part 2:", part2)