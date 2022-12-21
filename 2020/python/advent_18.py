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
tot = 0

def evaluate(line, index):
    subsum = 0
    operator = "+"
    i = index
    while i < len(line):
        char = line[i]
        if char == "(":
            nextindex, subphrase = evaluate(line, i+1)
            subsum = apply(operator, subsum, subphrase)
            i = nextindex
        elif char == ")":
            return i+1,subsum
        elif char == '*':
            operator = "*"
            i += 1
        elif char == '+':
            operator = "+"
            i += 1
        elif char == ' ':
            i += 1
        else:
            subsum = apply(operator, subsum, int(char))
            i += 1
    return i, subsum


def apply(operator, subsum, num):
    if operator == '*':
        return subsum * num
    else:
        return subsum + num

for line in inpt:
    _,linesum = evaluate(line, 0)
    tot += linesum

print("Part 1:", tot)

tot = 0
for line in inpt:
    line = re.sub(r"\(", "((((", line)
    line = re.sub(r"\)", "))))", line)
    line = re.sub(r"\*", "))*((", line)
    line = re.sub(r"\+", ")+(", line)
    line = re.sub(r" ", "", line)
    line = "((" + line + "))"
    _,linesum = evaluate(line, 0)
    tot += linesum

print("Part 2:", tot)
