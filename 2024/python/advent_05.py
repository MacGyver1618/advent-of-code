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

lines = full_input(5)
rules,print_jobs=lines.split("\n\n")
rules = [[*map(int, rule.split("|"))] for rule in rules.split("\n")]
print_jobs=print_jobs.strip().split("\n")

R = len(lines)
C = len(lines[0])

def in_order(pages):
    for a,b in rules:
        if a in pages and b in pages:
            if pages.index(a)>pages.index(b):
                return False
    return True

def order(pages):
    while not in_order(pages):
        for a,b in rules:
            if a in pages and b in pages:
                i,j=map(pages.index, (a,b))
                if i>j:
                    pages[i]=b
                    pages[j]=a
    return pages

part1=0
part2=0

for job in print_jobs:
    pages=[*map(int,job.split(","))]
    if in_order(pages):
        part1+=pages[len(pages)//2]
    else:
        ordered=order(pages)
        part2+=ordered[len(pages)//2]

print("Part 1:", part1)
print("Part 2:", part2)
