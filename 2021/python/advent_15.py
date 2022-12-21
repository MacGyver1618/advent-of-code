from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(15)

grid = {}
Y = len(inpt)
X = len(inpt[0])

for y, line in enumerate(inpt):
    for x, c in enumerate(line):
        grid[x,y] = int(c)

start = 0,0
goal = (X-1,Y-1)

def heur_fn(pos):
    return manhattan_distance(pos, goal)

def neighbors(p):
    return [tuple(n) for n in adjacent(p) if (n >= O).all() and (n < (X,Y)).all()]

part1 = a_star(start, lambda p: p == goal, neighbors, lambda _,p: grid[p], heur_fn)

print("Part 1:", sum(map(lambda p: grid[p], part1))-1)

goal = (5*X-1,5*Y-1)

def neighbors_2(p):
    return [tuple(n) for n in adjacent(p) if (n >= O).all() and (n < (5*X,5*Y)).all()]

def dist_fn(p):
    x,y = p
    fx = x // X
    fy = y // Y
    rx = x % X
    ry = y % Y
    orig = grid[rx,ry]
    return (orig + fx + fy - 1) % 9 + 1

part2 = a_star(start, lambda p: p == goal, neighbors_2, lambda _,p: dist_fn(p), heur_fn)

print("Part 2:", sum(map(dist_fn, part2))-1)
