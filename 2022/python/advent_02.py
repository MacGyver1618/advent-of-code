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

inpt = read_lines(2)

points = {
    "A X": 3+1,
    "A Y": 6+2,
    "A Z": 0+3,
    "B X": 0+1,
    "B Y": 3+2,
    "B Z": 6+3,
    "C X": 6+1,
    "C Y": 0+2,
    "C Z": 3+3,
}

points2 = {
    "A X": 0+3,
    "A Y": 3+1,
    "A Z": 6+2,
    "B X": 0+1,
    "B Y": 3+2,
    "B Z": 6+3,
    "C X": 0+2,
    "C Y": 3+3,
    "C Z": 6+1,
}

part1 = sum(points[line] for line in inpt)

print("Part 1:", part1)

part2 = sum(points2[line] for line in inpt)

print("Part 2:", part2)

# One-liners
print(sum(["XYZ".index(me) + 1 + [0,3,6][("XYZ".index(me)-"ABC".index(op)+1)%3] for op, me in [line.split() for line in inpt]]))
print(sum([3*"XYZ".index(me) + "ABC".index("ABC"[("ABC".index(op)+"XYZ".index(me)-1)%3])+1 for op, me in [line.split() for line in inpt]]))