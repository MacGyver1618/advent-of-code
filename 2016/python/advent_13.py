import heapq

from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(13)
fav = int(inpt[0])

def ptos(p):
    x,y = int(p.real), int(p.imag)
    d = x*x + 3*x + 2*x*y + y + y*y + fav
    bits = sum([1 for c in str("{0:b}".format(d)) if c == '1'])
    return "." if bits % 2 == 0 else "#"

def h(p):
    d = 31+39j-p
    return abs(int(d.real)) + abs(int(d.imag))

start = 1+1j
goal = 31+39j

Q = coll.deque()
Q.append(start)
came_from = {}

def reconstruct_path(cur):
    path = coll.deque()
    path.append(cur)
    while cur in came_from:
        cur = came_from[cur]
        path.appendleft(cur)
    return path

def neighbors(p):
    for d in [1,-1,1j,-1j]:
        n = d+p
        if n.real >= 0 and n.imag >= 0 and ptos(n) == '.':
            yield n

g_score = coll.defaultdict(lambda: float('inf'))
g_score[start] = 0

f_score = coll.defaultdict(lambda: float('inf'))
f_score[start] = h(start)

while Q:
    Q = coll.deque(sorted(Q, key= lambda x: f_score[x]))
    cur = Q.popleft()
    if cur == goal:
        part1 = len(reconstruct_path(cur))-1
    for n in neighbors(cur):
        tentative_g = g_score[cur] + 1
        if tentative_g < g_score[n]:
            came_from[n] = cur
            g_score[n] = tentative_g
            f_score[n] = tentative_g + h(n)
            if n not in Q:
                Q.append(n)

print("Part 1:", part1)

Q = coll.deque()
Q.append(start)
dists = {start: 0}
seen = {start}

while Q:
    cur = Q.popleft()
    for n in neighbors(cur):
        if n not in seen:
            dist = dists[cur] + 1
            if dist > 50:
                continue
            dists[n] = dist
            Q.append(n)
            seen.add(n)

print("Part 2:", len(seen))
