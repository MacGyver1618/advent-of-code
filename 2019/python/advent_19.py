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

from intcode import IntCodeMachine

def probe(r,c):
    machine = IntCodeMachine.from_day_input(19)
    machine.input(c)
    machine.input(r)
    machine.run()
    return machine.read()

grid=dict()
for r in range(50):
    s=""
    for c in range(50):
        result=probe(r,c)
        s+="#" if result else " "
        grid[r,c]=result
    print(s)

part1 = sum(grid.values())
print("Part 1:", part1)

r=c=0
while not probe(r,c+99):
    r+=1
    while not probe(r+99,c):
        c+=1
part2=c*10_000+r
print("Part 2:", part2)
