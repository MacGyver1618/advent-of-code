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

chunks = full_input(25)[:-1].split("\n\n")

init=chunks[0].split("\n")
start_state=init[0].split()[-1][:-1]
steps=int(init[1].split()[-2])

states=dict()
for chunk in chunks[1:]:
    lines=[line[:-1].split()[-1] for line in chunk.split("\n")]
    state=lines[0]
    when_0 = tuple(lines[i] for i in [2,3,4])
    when_1 = tuple(lines[i] for i in [6,7,8])
    states[state]=(when_0,when_1)

tape=defaultdict(int)
pos=0
state=start_state
for _ in range(steps):
    value=tape[pos]
    write,direction,next_state=states[state][value]
    tape[pos]=int(write)
    pos+=1 if direction=="right" else -1
    state=next_state

part1 = sum(tape.values())
print("Part 1:", part1)

part2 = "All done!"
print("Part 2:", part2)
