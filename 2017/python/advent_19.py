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

lines = read_lines(19)
grid = [list(line) for line in lines]
R=len(grid)*1j
C=len(grid[0])
pos = [i for i,c in enumerate(grid[0]) if c!=" "][0]
d=1j

def char_at(pos):
    return grid[int(pos.imag)][int(pos.real)]

s=""
steps=0
while True:
    char=char_at(pos)
    if char.isalpha():
        s+=char
    elif char == '+':
        if char_at(pos + 1j*d) in ABC + "+-|":
            d = 1j*d
        else:
            d = -1j*d
    pos=pos+d
    steps+=1
    if char_at(pos) not in ABC+"+-|":
        break

part1 = s
print("Part 1:", part1)

part2 = steps
print("Part 2:", part2)
