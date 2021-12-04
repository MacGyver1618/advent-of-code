from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(12)

pc = 0
regs = {
    "a": 0,
    "b": 0,
    "c": 0,
    "d": 0
}

while pc < len(inpt):
    op, *args = inpt[pc].split()
    x = args[0]
    y = args[1] if len(args) > 1 else ""
    if op == "cpy":
        regs[y] = regs[x] if x in regs else int(x)
        pc += 1
    if op == "inc":
        regs[x] += 1
        pc += 1
    if op == "dec":
        regs[x] -= 1
        pc += 1
    if op == "jnz":
        val = regs[x] if x in regs else int(x)
        pc += int(y) if val != 0 else 1

print("Part 1:", regs["a"])

pc = 0
regs = {
    "a": 0,
    "b": 0,
    "c": 1,
    "d": 0
}

while pc < len(inpt):
    op, *args = inpt[pc].split()
    x = args[0]
    y = args[1] if len(args) > 1 else ""
    if op == "cpy":
        regs[y] = regs[x] if x in regs else int(x)
        pc += 1
    if op == "inc":
        regs[x] += 1
        pc += 1
    if op == "dec":
        regs[x] -= 1
        pc += 1
    if op == "jnz":
        val = regs[x] if x in regs else int(x)
        pc += int(y) if val != 0 else 1
print("Part 2:", regs["a"])
