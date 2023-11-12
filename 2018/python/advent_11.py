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

lines = read_lines(11)
serial=int(lines[0])
grid=defaultdict(int)
for r in range(1,301):
    for c in range(1,301):
        rack_id=c+10
        power_level=rack_id*r
        power_level+=serial
        power_level*=rack_id
        power_level=power_level%1000//100
        power_level-=5
        grid[(r,c)]=power_level

max_power=float("-inf")
max_cell=0,0
for r in range(1,298):
    for c in range(1,298):
        square_power=sum(grid[(y,x)] for x in range(c,c+3) for y in range(r,r+3))
        if square_power>max_power:
            max_power=square_power
            max_cell=c,r

part1 = max_cell
print("Part 1:", part1)

cum_sum=defaultdict(int)
for r in range(1,301):
    for c in range(1,301):
        cum_sum[c,r]=cum_sum[c-1,r]+cum_sum[c,r-1]+grid[r,c]-cum_sum[c-1,r-1]

max_sum=float("-inf")
max_p=0,0,0
for w in range(1, 301):
    for x in range(0, 301-w):
        for y in range(0, 301-w):
            xmax=x+w-1
            ymax=y+w-1
            cur_sum=cum_sum[xmax,ymax]
            cur_sum-=cum_sum[x-1,ymax]
            cur_sum-=cum_sum[xmax,y-1]
            cur_sum+=cum_sum[x-1,y-1]
            if cur_sum > max_sum:
                max_sum=cur_sum
                max_p=x,y,w
print("Part 2:", max_p)
