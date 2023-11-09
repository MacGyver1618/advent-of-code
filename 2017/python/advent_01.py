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

lines = read_lines(1)
line = [*map(int,lines[0])]
part1 = sum(line[i] for i in range(len(line)) if line[i]==line[i-1])
print("Part 1:", part1)

part2 = sum(line[i] for i in range(len(line)) if line[i]==line[i-len(line)//2])
print("Part 2:", part2)
