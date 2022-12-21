from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(18)

rows = inpt.copy()

traps = [
    "..^",
    ".^^",
    "^^.",
    "^.."
]

def gen_next(line):
    padded = "." + line + "."
    return "".join(["^" if s in traps else "." for s in [padded[i-1:i+2] for i in range(1, len(padded)-1)]])

while len(rows) < 40:
    rows.append(gen_next(rows[-1]))

print("Part 1:", "".join(rows).count("."))

while len(rows) < 400_000:
    rows.append(gen_next(rows[-1]))

print("Part 2:", "".join(rows).count("."))
