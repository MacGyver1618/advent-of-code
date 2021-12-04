from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(23)

def run(regs):
    pc = 0
    while pc < len(inpt):
        op, val = inpt[pc].split(" ", maxsplit=1)
        if op == "hlf":
            regs[val]  //= 2
            pc += 1
        elif op == "tpl":
            regs[val] *= 3
            pc += 1
        elif op == "inc":
            regs[val] += 1
            pc += 1
        elif op == "jmp":
            pc += int(val)
        elif op == "jie":
            reg, jump = val.split(", ")
            pc += int(jump) if regs[reg] % 2 == 0 else 1
        elif op == "jio":
            reg, jump = val.split(", ")
            pc += int(jump) if regs[reg] == 1 else 1
    return regs["b"]

print("Part 1:", run({"a": 0, "b": 0}))
print("Part 2:", run({"a": 1, "b": 0}))
