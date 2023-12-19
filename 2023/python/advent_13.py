import copy

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

patterns = full_input(13)[:-1].split("\n\n")

def parse_pattern(pattern):
    return [[c for c in row] for row in pattern.split("\n")]

def score_pattern(pattern):
    rows=pattern
    score=0
    refrows,refcols=[],[]
    for i, row in enumerate(rows):
        start = i
        length = min(len(rows) - i, i)
        if rows[:start][::-1][:length] == rows[start:start + length]:
            score += i * 100
            if i>0:
                refrows+=[i]
    for i in range(len(rows[0])):
        start = i
        length = min(len(rows[0]) - i, i)
        if all(row[:start][::-1][:length] == row[start:start + length] for row in rows):
            score += i
            if i>0:
                refcols+=[i]
    return score,refrows,refcols

part1= sum(score_pattern(parse_pattern(p))[0] for p in patterns)
print("Part 1:", part1)

def perms(pattern):
    R=len(pattern)
    C=len(pattern[0])
    for r in range(R):
        for c in range(C):
            perm=copy.deepcopy(pattern)
            char = perm[r][c]
            perm[r][c]="#."[".#".index(char)]
            yield perm

tot=0
l=len(patterns)
for i,pattern in enumerate(patterns):
    changed_rows=set()
    changed_cols=set()
    parsed=parse_pattern(pattern)
    orig,orows,ocols=score_pattern(parsed)
    for perm in perms(parsed):
        score,rows,cols=score_pattern(perm)
        if rows and rows!=orows:
            changed_rows.update([row for row in rows if row not in orows])
            break
        if cols and cols!=ocols:
            changed_cols.update([col for col in cols if col not in ocols])
            break
    tot+=100*sum(changed_rows)+sum(changed_cols)
part2=tot
print("Part 2:", part2)
