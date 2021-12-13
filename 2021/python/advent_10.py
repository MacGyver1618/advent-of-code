from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(10)

penalties = {
    ")": ("(", 3),
    "]": ("[", 57),
    "}": ("{", 1197),
    ">": ("<", 25137),
}

def syntax_score(line):
    stack = coll.deque()
    for c in line:
        if c in "([{<":
            stack.append(c)
        if c in ")]}>":
            o = stack.pop()
            m, penalty = penalties[c]
            if o != m:
                return penalty
    return 0

score = 0
incomplete = []

for line in inpt:
    s = syntax_score(line)
    if s == 0:
        incomplete.append(line)
    score += s

part1 = score
print("Part 1:", part1)

def completion_score(line):
    stack = coll.deque()
    for c in line:
        if c in "([{<":
            stack.append(c)
        if c in ")]}>":
            stack.pop()
    s = 0
    while stack:
        s *= 5
        s += "([{<".index(stack.pop()) + 1
    return s

scores = []

for line in incomplete:
    scores.append(completion_score(line))

part2 = list(sorted(scores))[len(scores) // 2]
print("Part 2:", part2)
