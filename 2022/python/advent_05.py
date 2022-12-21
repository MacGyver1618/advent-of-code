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

lines = read_lines(5)

stacks_in = lines[:8]
instrs = lines[10:]

stacks_in[0] += " "*8
def solve(part2 = False):
    stacks = [deque() for _ in range(9)]
    for r in range(8):
        for c in range(9):
            box = stacks_in[r][4*c+1]
            if box != " ":
                stacks[c].append(box)
    for instr in instrs:
        amt, frm, to = map(int, re.findall(r"\d+", instr))
        moved = deque()
        for _ in range(amt):
            box = stacks[frm-1].popleft()
            moved.appendleft(box)
        for _ in range(amt):
            box = moved.popleft() if part2 else moved.pop()
            stacks[to-1].appendleft(box)
    res = ""
    for stack in stacks:
        res += stack[0]
    return res

print("Part 1:", solve())
print("Part 2:", solve(part2=True))
