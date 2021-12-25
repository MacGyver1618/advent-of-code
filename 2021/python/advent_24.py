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
import math

prog = lines(24)

def validate(number):
    pc = 0
    regs = {
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0,
    }
    for line in prog:
        op, *rest = line.split()
        if op == "inp":
            regs[rest[0]] = int(number[pc])
            pc += 1
        else:
            a,b = rest
            tgt = a
            a = regs[a]
            b = regs[b] if b in regs else int(b)
            if op == "add":
                regs[tgt] = a + b
            elif op == "mul":
                regs[tgt] = a * b
            elif op == "div":
                regs[tgt] = math.trunc(a/b)
            elif op == "mod":
                regs[tgt] = a % b
            elif op == "eql":
                regs[tgt] = 1 if a == b else 0
    return regs

def opt(n):
    w = [int(x) for x in str(n)]
    # read w[0]
    z = w[0] + 16
    # read w[1]
    x = z % 26 + 11 != w[1]
    y = 25*x+1
    z *= y
    z += w[1] + 3
    # read w[2]
    x = z % 26 + 12 != w[2]
    y = 25*x + 1
    z *= y
    y = x*(w[2] + 2)
    z += y
    # read w[3]
    x = z % 26 + 11 != w[3]
    y = 25*x + 1
    z *= y
    y = x*(w[3] + 7)
    z += y
    # read w[4]
    x = (z % 26 - 10) != w[4]
    z //= 26
    y = 25*x + 1
    z *= y
    y = x*(w[4] + 13)
    z += y
    # read w[5]
    x = z % 26 + 15 != w[5]
    y = 25*x + 1
    z *= y
    y = x*(w[5] + 6)
    z += y
    # read w[6]
    x = z % 26 - 14 != w[6]
    z //= 26
    y = 25*x + 1
    z *= y
    y = w[6] + 10
    y *= x
    z += y
    # read w[7]
    x = (z % 26) + 10 != w[7]
    y = 25*x + 1
    z *= y
    y = w[7] + 11
    y *= x
    z += y
    # read w[8]
    x = z % 26
    z //= 26
    x = x - 4 != w[8]
    y = 25*x + 1
    z *= y
    y = w[8] + 6
    y *= x
    z += y
    # read w[9]
    x = z % 26
    z //= 26
    x = x - 3 != w[9]
    y = 25*x + 1
    z *= y
    y = w[9] + 5
    y *= x
    z += y
    # read w[10]
    x = (z % 26) + 13 != w[10]
    y = 25*x + 1
    z *= y
    y = w[10] + 11
    y *= x
    z += y
    # read w[11]
    x = z % 26
    z //= 26
    x = x - 3 != w[11]
    y = 25*x + 1
    z *= y
    y = w[11] + 4
    y *= x
    z += y
    # read w[12]
    x = z % 26
    z //= 26
    x = x -9 != w[12]
    y = 25*x + 1
    z *= y
    y = w[12] + 4
    y *= x
    z += y
    # read w[13]
    x = z % 26
    z //= 26
    x = x - 12 != w[13]
    y = 25*x + 1
    z *= y
    y = w[13] + 6
    y *= x
    z += y

    return z

pairs = [
    ( 14,16), #  0
    ( 11, 3), #  1
    ( 12, 2), #  2
    ( 11, 7), #  3
    (-10,13), #  4
    ( 15, 6), #  5
    (-14,10), #  6
    ( 10,11), #  7
    ( -4, 6), #  8
    ( -3, 5), #  9
    ( 13,11), # 10
    ( -3, 4), # 11
    ( -9, 4), # 12
    (-12, 6), # 13
]

def opt2(n):
    ws = [int(x) for x in str(n)]
    z = 0
    for i,(a,b) in enumerate(pairs):
        w = ws[i]
        x = z % 26 + a != w
        if a < 0:
            z //= 26
        if x:
            z = 26*z + w + b
    return z

stack = []
number = {}
for cur, (a2,b2) in enumerate(pairs):
    if a2 > 0:
        stack.append((cur,a2,b2))
    else:
        prev,a1,b1 = stack.pop()
        d = a2 + b1
        if d < 0:
            number[prev] = 9
            number[cur] = 9 + d
        else:
            number[prev] = 9 - d
            number[cur] = 9

print("Part 1:", "".join([str(number[i]) for i in range(14)]))

stack = []
number = {}
for cur, (a2,b2) in enumerate(pairs):
    if a2 > 0:
        stack.append((cur,a2,b2))
    else:
        prev,a1,b1 = stack.pop()
        d = a2 + b1
        if d < 0:
            number[prev] = 1 - d
            number[cur] = 1
        else:
            number[prev] = 1
            number[cur] = 1 + d

print("Part 2:", "".join([str(number[i]) for i in range(14)]))